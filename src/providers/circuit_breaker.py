"""A closed/open/half-open circuit guarding a flaky provider.

Without a breaker, a provider that is down turns every incoming request
into a chain of timeouts and retries, each holding a worker. Under
concurrency that exhausts the pool and the whole API degrades even for
requests that never touch the provider. The breaker stops sending
traffic to a provider that is already known to be failing, and lets it
probe recovery after a cool-down.

State transitions:

    failures < threshold        OPEN  -> after recovery  HALF_OPEN
                                HALF_OPEN -> success        CLOSED
                                HALF_OPEN -> failure        OPEN
                                CLOSED  -> failures == threshold  OPEN
"""

from enum import StrEnum
from time import monotonic

from src.core.exceptions import CircuitOpenError


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_seconds: float = 30.0,
    ) -> None:
        if failure_threshold <= 0:
            raise ValueError("failure_threshold must be greater than zero")

        if recovery_seconds <= 0:
            raise ValueError("recovery_seconds must be greater than zero")

        self._failure_threshold = failure_threshold
        self._recovery_seconds = recovery_seconds

        self._failures = 0
        self._opened_at: float | None = None
        self._state = CircuitState.CLOSED

    @property
    def state(self) -> CircuitState:
        # The OPEN -> HALF_OPEN transition is derived from elapsed time
        # rather than applied by a background timer, so a breaker that
        # has sat idle for longer than the recovery window reports
        # HALF_OPEN on the next inspection without needing a task.
        if self._state == CircuitState.OPEN:
            if (
                self._opened_at is not None
                and monotonic() - self._opened_at
                >= self._recovery_seconds
            ):
                self._state = CircuitState.HALF_OPEN

        return self._state

    @property
    def failure_count(self) -> int:
        return self._failures

    def before_call(self) -> None:
        """Raise if the provider should not be called right now."""
        if self.state == CircuitState.OPEN:
            raise CircuitOpenError(
                "The generation provider is temporarily unavailable."
            )

    def record_success(self) -> None:
        self._failures = 0
        self._opened_at = None
        self._state = CircuitState.CLOSED

    def record_failure(self) -> None:
        self._failures += 1

        # A failure during the HALF_OPEN probe re-opens the circuit
        # immediately instead of waiting for the threshold again: the
        # provider was given a fresh chance and did not take it.
        if (
            self._state == CircuitState.HALF_OPEN
            or self._failures >= self._failure_threshold
        ):
            self._state = CircuitState.OPEN
            self._opened_at = monotonic()