<p class="lead">Seven short, tested implementations of the mechanisms that are easy to
describe and hard to get right.</p>

# Code samples

These are teaching implementations, not libraries. Each is forty to a hundred lines, has no
dependencies beyond the standard library, and is covered by a test. The point is to make the
failure modes concrete: you can watch a token bucket refuse the eleventh request, or watch a
circuit breaker refuse to touch a dependency it has decided is dead.

| Sample | The thing it gets right |
| --- | --- |
| [Retry with backoff](retry.md) | Full jitter, a time budget, and retrying only what is safe |
| [Token bucket](token-bucket.md) | One atomic check-and-decrement, and a burst allowance |
| [Circuit breaker](circuit-breaker.md) | Minimum volume, half-open probes, a fallback |
| [Idempotency store](idempotency.md) | Atomic claim, stored response, in-flight handling |
| [Consistent hashing](consistent-hashing.md) | Virtual nodes, and a replication set |
| [Shard router](sharding.md) | Logical shards, and minimal movement when growing |
| [LRU cache](lru-cache.md) | O(1) recency, and expiry as distinct from eviction |

## Running them

```bash
git clone https://github.com/vkdev01/system-design-guide.git
cd system-design-guide
pip install pytest
pytest -q code/python/tests
```

All 24 tests run in well under a second, because clocks and random number generators are
injected rather than slept on. That is also a design lesson: code you cannot test deterministically
is code you will not test.

## A note on scope

Nothing here is thread-safe enough, observable enough, or configurable enough for production. Each
sample isolates one decision so you can see it clearly. The production versions of these live in
your language's standard library, in Envoy, in Redis, and in every HTTP client you already use.
