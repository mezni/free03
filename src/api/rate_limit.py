"""In-process fixed-window rate limiting.

This limiter keeps counters in the worker's own memory. That has one
consequence worth stating plainly, because it is invisible until it
causes an incident:

    API instance 1  ->  limiter A  (60/min)
    API instance 2  ->  limiter B  (60/min)
    API instance 3  ->  limiter C  (60/min)

A client sending 200 requests/minute is rejected by each instance
independently, so the effective global limit is 60/min *per instance*.
Nothing here coordinates across instances. Multiple workers in one
process have the same limitation, and `production.workers` is 2 by
default.

A horizontally scaled deployment needs a shared store (typically Redis)
with atomic increment. That is deliberately out of scope here.
"""

import time
from collections import OrderedDict
from typing import Protocol


class RateLimiter(Protocol):
    def allow(self, client_id: str) -> bool:
        """Record a request and report whether it is permitted."""


class InMemoryRateLimiter:
    """Sliding-window limiter bounded in both time and memory.

    Two bounds the obvious implementation omits:

    - Clients that have gone quiet are evicted, so the key set cannot
      grow without limit just from scanning an arbitrary IP range.
    - The key set is capped at `max_clients`. An unbounded map keyed by
      client address is a trivial memory-exhaustion vector.
    """

    def __init__(
        self,
        requests_per_minute: int,
        max_clients: int = 10_000,
        window_seconds: float = 60.0,
        monotonic: type[time] | None = None,
    ) -> None:
        if requests_per_minute <= 0:
            raise ValueError(
                "requests_per_minute must be greater than zero"
            )

        if max_clients <= 0:
            raise ValueError("max_clients must be greater than zero")

        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        self._limit = requests_per_minute
        self._max_clients = max_clients
        self._window_seconds = window_seconds
        self._clock = time.monotonic
        self._requests: OrderedDict[str, list[float]] = OrderedDict()

    def allow(self, client_id: str) -> bool:
        now = self._clock()
        window_start = now - self._window_seconds

        timestamps = [
            timestamp
            for timestamp in self._requests.get(client_id, ())
            if timestamp > window_start
        ]

        if len(timestamps) >= self._limit:
            # Recorded without a new timestamp: the rejected attempt
            # must not extend the client's own window.
            self._requests[client_id] = timestamps
            self._requests.move_to_end(client_id)

            return False

        timestamps.append(now)

        self._requests[client_id] = timestamps
        self._requests.move_to_end(client_id)

        self._evict_idle(now)

        return True

    def _evict_idle(self, now: float) -> None:
        window_start = now - self._window_seconds

        for client_id in [
            client_id
            for client_id, timestamps in self._requests.items()
            if not timestamps or timestamps[-1] <= window_start
        ]:
            del self._requests[client_id]

        while len(self._requests) > self._max_clients:
            self._requests.popitem(last=False)

    @property
    def tracked_clients(self) -> int:
        return len(self._requests)