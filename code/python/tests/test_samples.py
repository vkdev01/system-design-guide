"""Tests for the sample implementations.

    pytest -q code/python/tests

Everything here is deterministic: clocks and RNGs are injected, so there is no
sleeping and no flakiness.
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from circuit_breaker import CircuitBreaker, CircuitOpenError, State  # noqa: E402
from consistent_hash import HashRing  # noqa: E402
from idempotency import IdempotencyStore, Outcome  # noqa: E402
from lru_cache import LRUCache  # noqa: E402
from retry import RetryPolicy, retry  # noqa: E402
from shard_router import ShardRouter  # noqa: E402
from token_bucket import TokenBucket  # noqa: E402


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


# ---------------------------------------------------------------- retry -----
def test_retry_succeeds_after_transient_failures():
    sleeps = []
    attempts = {"n": 0}

    @retry(policy=RetryPolicy(attempts=4, base=0.1, cap=1.0, budget=10),
           sleep=sleeps.append, rng=__import__("random").Random(0))
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise TimeoutError("boom")
        return "ok"

    assert flaky() == "ok"
    assert attempts["n"] == 3
    assert len(sleeps) == 2
    assert all(0 <= d <= 0.4 for d in sleeps)  # jitter stays under the ceiling


def test_retry_does_not_catch_non_retryable_errors():
    attempts = {"n": 0}

    @retry(policy=RetryPolicy(attempts=3), sleep=lambda _: None)
    def bad_request():
        attempts["n"] += 1
        raise ValueError("400")

    with pytest.raises(ValueError):
        bad_request()
    assert attempts["n"] == 1  # no retries


def test_retry_gives_up_after_max_attempts():
    attempts = {"n": 0}

    @retry(policy=RetryPolicy(attempts=3, base=0.0, cap=0.0, budget=10),
           sleep=lambda _: None)
    def always_fails():
        attempts["n"] += 1
        raise ConnectionError("nope")

    with pytest.raises(ConnectionError):
        always_fails()
    assert attempts["n"] == 3


# --------------------------------------------------------- token bucket -----
def test_token_bucket_allows_burst_then_denies():
    clock = FakeClock()
    bucket = TokenBucket(capacity=5, refill_per_sec=1, clock=clock)
    assert all(bucket.allow() for _ in range(5))
    assert bucket.allow() is False
    clock.advance(1)
    assert bucket.allow() is True
    assert bucket.allow() is False


def test_token_bucket_retry_after():
    clock = FakeClock()
    bucket = TokenBucket(capacity=1, refill_per_sec=2, clock=clock)
    assert bucket.allow() is True
    assert bucket.retry_after() == pytest.approx(0.5)


def test_token_bucket_never_exceeds_capacity():
    clock = FakeClock()
    bucket = TokenBucket(capacity=3, refill_per_sec=100, clock=clock)
    clock.advance(60)
    assert bucket.tokens == 3  # capped, not 6000


# ------------------------------------------------------ circuit breaker -----
def test_breaker_opens_after_threshold_and_fails_fast():
    clock = FakeClock()
    breaker = CircuitBreaker(failure_threshold=0.5, min_volume=4, window=10,
                             cooldown=5, clock=clock)

    def boom():
        raise RuntimeError("dependency down")

    for _ in range(4):
        with pytest.raises(RuntimeError):
            breaker.call(boom)
    assert breaker.state is State.OPEN
    with pytest.raises(CircuitOpenError):
        breaker.call(boom)


def test_breaker_uses_fallback_while_open():
    clock = FakeClock()
    breaker = CircuitBreaker(failure_threshold=0.5, min_volume=2, window=10,
                             cooldown=5, clock=clock)

    def boom():
        raise RuntimeError("down")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            breaker.call(boom)
    assert breaker.call(boom, fallback=lambda: "cached") == "cached"


def test_breaker_half_open_then_closes_on_success():
    clock = FakeClock()
    breaker = CircuitBreaker(failure_threshold=0.5, min_volume=2, window=10,
                             cooldown=5, half_open_probes=1, clock=clock)

    def boom():
        raise RuntimeError("down")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            breaker.call(boom)
    clock.advance(6)
    assert breaker.call(lambda: "recovered") == "recovered"
    assert breaker.state is State.CLOSED


def test_breaker_does_not_open_on_low_volume():
    clock = FakeClock()
    breaker = CircuitBreaker(failure_threshold=0.5, min_volume=10, clock=clock)
    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("x")))
    assert breaker.state is State.CLOSED


# ----------------------------------------------------------- idempotency ---
def test_idempotency_replay_returns_original_response():
    store = IdempotencyStore()
    calls = {"n": 0}

    def charge():
        calls["n"] += 1
        return 201, {"payment_id": "p1"}

    first = store.execute("payments", "k1", charge)
    second = store.execute("payments", "k1", charge)
    assert first == second == (201, {"payment_id": "p1"})
    assert calls["n"] == 1  # the work happened once


def test_idempotency_in_flight_is_rejected():
    store = IdempotencyStore()
    assert store.claim("payments", "k2")[0] is Outcome.FRESH
    assert store.claim("payments", "k2")[0] is Outcome.IN_FLIGHT


def test_idempotency_failure_releases_the_claim():
    store = IdempotencyStore()

    def fail():
        raise RuntimeError("provider timeout")

    with pytest.raises(RuntimeError):
        store.execute("payments", "k3", fail)
    assert store.claim("payments", "k3")[0] is Outcome.FRESH  # retry allowed


def test_idempotency_keys_are_scoped():
    store = IdempotencyStore()
    assert store.claim("payments", "shared")[0] is Outcome.FRESH
    assert store.claim("refunds", "shared")[0] is Outcome.FRESH


# ------------------------------------------------------ consistent hashing --
def test_ring_is_stable_when_a_node_is_added():
    keys = [f"user:{i}" for i in range(2000)]
    ring = HashRing(["n1", "n2", "n3", "n4"], vnodes=100)
    before = {k: ring.get(k) for k in keys}
    ring.add("n5")
    after = {k: ring.get(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    # adding the 5th node should move roughly 1/5 of keys, not almost all
    assert 0.12 < moved / len(keys) < 0.28


def test_ring_distribution_is_reasonably_even():
    ring = HashRing(["a", "b", "c", "d"], vnodes=150)
    dist = ring.distribution(f"k{i}" for i in range(8000))
    counts = list(dist.values())
    assert min(counts) > 0.15 * 2000  # no node starved
    assert max(counts) < 0.35 * 8000  # no node overloaded


def test_replication_set_has_distinct_nodes():
    ring = HashRing(["a", "b", "c"], vnodes=50)
    replicas = ring.get_nodes("some-key", count=3)
    assert len(replicas) == 3
    assert len(set(replicas)) == 3


# --------------------------------------------------------- shard router ----
def test_shard_router_is_deterministic():
    router = ShardRouter(logical_shards=64, nodes=["n1", "n2"])
    assert router.node_for("tenant:42") == router.node_for("tenant:42")


def test_adding_a_node_moves_only_a_slice():
    router = ShardRouter(logical_shards=1024, nodes=["n1", "n2", "n3", "n4"])
    before = {i: router._shard_to_node[i] for i in range(1024)}
    router.add_node("n5")
    moved = sum(1 for i in range(1024) if router._shard_to_node[i] != before[i])
    assert 150 < moved < 300  # about 1/5 of 1024


def test_plan_add_node_has_no_side_effects():
    router = ShardRouter(logical_shards=128, nodes=["n1", "n2"])
    before = dict(router._shard_to_node)
    moved = router.plan_add_node("n3")
    assert router._shard_to_node == before
    assert sum(len(v) for v in moved.values()) > 0


# ------------------------------------------------------------- lru cache ---
def test_lru_evicts_least_recently_used():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")          # "a" is now more recent than "b"
    cache.put("c", 3)       # evicts "b"
    assert cache.get("a") == 1
    assert cache.get("b") is None
    assert cache.get("c") == 3
    assert cache.evictions == 1


def test_lru_respects_ttl():
    clock = FakeClock()
    cache = LRUCache(capacity=10, clock=clock)
    cache.put("k", "v", ttl=5)
    assert cache.get("k") == "v"
    clock.advance(6)
    assert cache.get("k") is None
    assert cache.expirations == 1


def test_lru_hit_rate():
    cache = LRUCache(capacity=2)
    cache.put("x", 1)
    cache.get("x")
    cache.get("missing")
    assert cache.hit_rate == pytest.approx(0.5)


def test_shard_distribution_is_reasonably_even():
    router = ShardRouter(logical_shards=1024, nodes=["n1", "n2", "n3", "n4"])
    counts = {n: 0 for n in router.nodes}
    for shard, node in router._shard_to_node.items():
        counts[node] += 1
    assert min(counts.values()) > 150  # no node starved
    assert max(counts.values()) < 360  # no node overloaded
