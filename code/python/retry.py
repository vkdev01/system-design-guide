"""Exponential backoff with full jitter.

The point of this module is the jitter: without it, every client that failed at
the same moment retries at the same moment, and a recovering service is hit by
a synchronised wall of traffic.

Run the tests with:  pytest -q code/python/tests
"""

from __future__ import annotations

import functools
import random
import time
from dataclasses import dataclass
from typing import Callable, Tuple, Type


@dataclass(frozen=True)
class RetryPolicy:
    """How hard to try, and for how long.

    attempts: total tries, including the first one.
    base:     the first backoff interval, in seconds.
    cap:      the largest single sleep, in seconds.
    budget:   the total wall-clock time we are willing to spend retrying.
    """

    attempts: int = 4
    base: float = 0.05
    cap: float = 2.0
    budget: float = 5.0

    def delay(self, attempt: int, rng: random.Random | None = None) -> float:
        """Full jitter: a uniform draw from zero to the exponential ceiling."""
        rng = rng or random
        ceiling = min(self.cap, self.base * (2 ** attempt))
        return rng.uniform(0, ceiling)


def retry(
    policy: RetryPolicy | None = None,
    retryable: Tuple[Type[BaseException], ...] = (TimeoutError, ConnectionError),
    sleep: Callable[[float], None] = time.sleep,
    rng: random.Random | None = None,
) -> Callable:
    """Wrap a function so that transient failures are retried.

    Only exceptions in `retryable` are caught. Anything else -- a validation
    error, a 400, a bug -- propagates immediately, because retrying it cannot
    help. That distinction is the whole safety argument for retries.
    """
    policy = policy or RetryPolicy()

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            started = time.monotonic()
            for attempt in range(policy.attempts):
                try:
                    return fn(*args, **kwargs)
                except retryable:
                    is_last = attempt == policy.attempts - 1
                    if is_last:
                        raise
                    delay = policy.delay(attempt, rng)
                    if time.monotonic() - started + delay > policy.budget:
                        raise
                    sleep(delay)
            raise AssertionError("unreachable")

        return wrapper

    return decorator
