import time

import time
from typing import TypeVar

T = TypeVar("T")

"""Rate limiting and concurrency control for LLM provider requests.

This module provides two complementary controls:

1. TokenBucket — a thread-safe in-memory rate limiter that controls how
   frequently requests may start.
2. ConcurrencyLimiter — a semaphore-based limiter that caps how many
   requests may be in progress simultaneously.

Both are process-local. Distributed coordination is required for shared
quotas across multiple workers.
"""

import threading
from collections.abc import Callable


class TokenBucket:
    """Thread-safe in-memory token-bucket rate limiter."""

    def __init__(
        self,
        *,
        capacity: float,
        refill_rate_per_second: float,
        clock: Callable[[], float] = time.monotonic,
    ):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if refill_rate_per_second <= 0:
            raise ValueError("refill rate must be > 0")

        self.capacity = capacity
        self.refill_rate = refill_rate_per_second
        self.tokens = capacity
        self.clock = clock
        self.updated_at = clock()
        self.lock = threading.Lock()

    def try_acquire(self, tokens: float = 1.0) -> bool:
        """Attempt to acquire ``tokens`` from the bucket.

        Returns ``True`` if tokens were consumed, ``False`` if insufficient
        tokens are available (the bucket does not block).
        """
        if tokens <= 0:
            raise ValueError("tokens requested must be > 0")
        if tokens > self.capacity:
            raise ValueError("requested tokens exceed bucket capacity")

        with self.lock:
            now = self.clock()
            elapsed = max(0.0, now - self.updated_at)

            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.refill_rate,
            )
            self.updated_at = now

            if self.tokens < tokens:
                return False

            self.tokens -= tokens
            return True


class ConcurrencyLimitExceededError(RuntimeError):
    """Raised when the concurrency limiter cannot acquire a permit."""


class ConcurrencyLimiter:
    """Limit simultaneous operations in one process.

    Uses a ``threading.BoundedSemaphore`` internally.  The ``run()`` method
    acquires a permit, executes the given operation, and guarantees release
    via a ``finally`` block, even when the operation raises.
    """

    def __init__(self, max_concurrent: int):
        if max_concurrent < 1:
            raise ValueError("max_concurrent must be >= 1")

        self.semaphore = threading.BoundedSemaphore(max_concurrent)

    def run(
        self,
        operation: Callable[[], T],
        *,
        acquire_timeout_seconds: float = 0.0,
    ) -> T:
        """Execute ``operation`` within the concurrency limit.

        Raises :class:`ConcurrencyLimitExceededError`` if a permit cannot
        be acquired within ``acquire_timeout_seconds``.
        """
        acquired = self.semaphore.acquire(timeout=acquire_timeout_seconds)

        if not acquired:
            raise ConcurrencyLimitExceededError(
                "Maximum concurrent operations reached"
            )

        try:
            return operation()
        finally:
            self.semaphore.release()


class LocalRateLimitExceededError(RuntimeError):
    """Raised when the rate limiter has no tokens available.

    This is a typed exception so workers can distinguish rate-limit rejections
    from other failures and apply appropriate backpressure (e.g. reschedule the
    job with a future ``available_at`` timestamp).
    """