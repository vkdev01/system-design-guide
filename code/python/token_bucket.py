"""A token bucket rate limiter.

Tokens refill at a steady rate; each request takes one. `capacity` sets how
large a burst is allowed, `refill_per_sec` sets the sustained rate, and the two
are independent -- which is why this is the right default algorithm.

The single-process version here is the logic that a distributed implementation
must run atomically (in Redis, as one Lua script). Splitting the check and the
decrement into two operations is the bug that lets two requests both consume the
last token.
"""

from __future__ import annotations

import threading
import time
from typing import Callable


class TokenBucket:
    def __init__(
        self,
        capacity: float,
        refill_per_sec: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_per_sec < 0:
            raise ValueError("refill_per_sec cannot be negative")
        self.capacity = float(capacity)
        self.refill_per_sec = float(refill_per_sec)
        self._clock = clock
        self._tokens = float(capacity)
        self._last = clock()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = self._clock()
        elapsed = max(0.0, now - self._last)
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_per_sec)
        self._last = now

    def allow(self, tokens: float = 1.0) -> bool:
        """Consume `tokens` if available. One atomic step, under a lock."""
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    @property
    def tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens

    def retry_after(self, tokens: float = 1.0) -> float:
        """Seconds until the request would succeed. Useful for Retry-After."""
        with self._lock:
            self._refill()
            missing = tokens - self._tokens
            if missing <= 0:
                return 0.0
            if self.refill_per_sec == 0:
                return float("inf")
            return missing / self.refill_per_sec
