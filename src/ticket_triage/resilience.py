"""Resilience wrappers for the classification provider.

Three mechanisms compose here:

- :class:`RetryingClassifier` asks "should I try this request again?" It retries
  only :class:`TransientProviderError` with bounded exponential backoff and full
  jitter, so transient failures recover without a retry storm. An optional
  overall deadline bounds the whole sequence of attempts, not just one call.
- :class:`CircuitBreakerClassifier` asks "should I call the provider at all right
  now?" It fails fast while the provider is unhealthy and probes cautiously for
  recovery.

Compose the breaker *outside* the retry wrapper so the breaker counts the final
result of one logical classification request rather than every individual retry.

Retrying an LLM classification is safe because classification only produces a
recommendation. Routing is different: an unknown routing outcome must be
reconciled, never blindly retried. Cancellation (a ``BaseException`` signal) is
never caught here, so it always propagates.
"""

import random
import threading
import time
from collections.abc import Callable
from enum import StrEnum

from ticket_triage.classification import Classifier
from ticket_triage.deadlines import (
    DeadlineExceededError,
    call_with_deadline,
    remaining_seconds,
)
from ticket_triage.domain import Recommendation, Ticket
from ticket_triage.errors import TransientProviderError


class RetryingClassifier:
    """Retry transient failures with full-jitter backoff, within a deadline."""

    def __init__(
        self,
        classifier: Classifier,
        *,
        max_attempts: int = 3,
        base_delay_seconds: float = 0.25,
        max_delay_seconds: float = 4.0,
        overall_timeout_seconds: float | None = None,
        max_attempt_timeout_seconds: float = 10.0,
        sleep: Callable[[float], None] = time.sleep,
        random_fn: Callable[[], float] = random.random,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")
        if base_delay_seconds < 0:
            raise ValueError("base_delay_seconds must be >= 0.")
        if max_delay_seconds < 0:
            raise ValueError("max_delay_seconds must be >= 0.")
        if not 0 <= base_delay_seconds <= max_delay_seconds:
            raise ValueError("base_delay_seconds must be <= max_delay_seconds.")
        if overall_timeout_seconds is not None and overall_timeout_seconds <= 0:
            raise ValueError("overall_timeout_seconds must be > 0.")
        if max_attempt_timeout_seconds <= 0:
            raise ValueError("max_attempt_timeout_seconds must be > 0.")

        self.classifier = classifier
        self.max_attempts = max_attempts
        self.base_delay_seconds = base_delay_seconds
        self.max_delay_seconds = max_delay_seconds
        self.overall_timeout_seconds = overall_timeout_seconds
        self.max_attempt_timeout_seconds = max_attempt_timeout_seconds
        self.sleep = sleep
        self.random_fn = random_fn
        self.clock = clock

    def classify(
        self,
        ticket: Ticket,
        *,
        timeout_seconds: float | None = None,
    ) -> Recommendation:
        deadline = self._deadline(timeout_seconds)

        for attempt in range(1, self.max_attempts + 1):
            try:
                return self._attempt(ticket, deadline)
            except TransientProviderError:
                if attempt == self.max_attempts:
                    raise
                self._backoff(attempt, deadline)

        raise AssertionError("Unreachable.")

    def _attempt(
        self,
        ticket: Ticket,
        deadline: float | None,
    ) -> Recommendation:
        if deadline is None:
            return self.classifier.classify(ticket)

        # Recompute the remaining budget on every attempt: never reuse an
        # earlier timeout, and never start an attempt with no budget left.
        return call_with_deadline(
            lambda attempt_timeout: self.classifier.classify(
                ticket,
                timeout_seconds=attempt_timeout,
            ),
            deadline=deadline,
            clock=self.clock,
            max_attempt_timeout_seconds=self.max_attempt_timeout_seconds,
        )

    def _backoff(self, attempt: int, deadline: float | None) -> None:
        # Exponential ceiling, capped, then full jitter in [0, ceiling).
        ceiling = min(
            self.max_delay_seconds,
            self.base_delay_seconds * (2 ** (attempt - 1)),
        )
        delay = self.random_fn() * ceiling

        if deadline is not None:
            remaining = remaining_seconds(deadline, clock=self.clock)
            # Do not sleep away the time another attempt needs.
            if delay >= remaining:
                raise DeadlineExceededError(
                    "Operation deadline leaves no time for another attempt"
                )
            delay = min(delay, remaining)

        self.sleep(delay)

    def _deadline(self, timeout_seconds: float | None) -> float | None:
        budgets = [
            value
            for value in (self.overall_timeout_seconds, timeout_seconds)
            if value is not None
        ]
        if not budgets:
            return None
        return self.clock() + min(budgets)


class CircuitOpenError(RuntimeError):
    """Raised when the circuit breaker blocks a provider call."""


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerClassifier:
    """Fail fast while the provider is unhealthy; probe before reopening."""

    def __init__(
        self,
        classifier: Classifier,
        *,
        failure_threshold: int = 3,
        reset_timeout_seconds: float = 30.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be >= 1.")
        if reset_timeout_seconds <= 0:
            raise ValueError("reset_timeout_seconds must be > 0.")

        self.classifier = classifier
        self.failure_threshold = failure_threshold
        self.reset_timeout_seconds = reset_timeout_seconds
        self.clock = clock

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.opened_at: float | None = None
        self.probe_in_flight = False
        self.lock = threading.Lock()

    def _before_call(self) -> bool:
        """Decide whether to allow the call. Return whether it is a probe."""
        with self.lock:
            now = self.clock()

            if self.state == CircuitState.OPEN:
                assert self.opened_at is not None
                if now - self.opened_at < self.reset_timeout_seconds:
                    raise CircuitOpenError("LLM circuit is open.")
                self.state = CircuitState.HALF_OPEN

            if self.state == CircuitState.HALF_OPEN:
                if self.probe_in_flight:
                    raise CircuitOpenError("LLM recovery probe already in progress.")
                self.probe_in_flight = True
                return True

            return False

    def _success(self) -> None:
        with self.lock:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.opened_at = None
            self.probe_in_flight = False

    def _transient_failure(self, was_probe: bool) -> None:
        with self.lock:
            self.probe_in_flight = False

            if was_probe:
                # The recovery probe failed: the provider is still unhealthy.
                self.state = CircuitState.OPEN
                self.opened_at = self.clock()
                return

            if self.state != CircuitState.CLOSED:
                return

            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                self.opened_at = self.clock()

    def _other_failure(self, was_probe: bool) -> None:
        # A non-transient error does not count toward the threshold: retrying or
        # opening the circuit will not fix invalid credentials or bad output.
        if not was_probe:
            return

        # A probe that failed for another reason has not demonstrated recovery.
        with self.lock:
            self.probe_in_flight = False
            self.state = CircuitState.OPEN
            self.opened_at = self.clock()

    def classify(
        self,
        ticket: Ticket,
        *,
        timeout_seconds: float | None = None,
    ) -> Recommendation:
        was_probe = self._before_call()

        try:
            result = self.classifier.classify(
                ticket,
                timeout_seconds=timeout_seconds,
            )
        except TransientProviderError:
            self._transient_failure(was_probe)
            raise
        except Exception:
            self._other_failure(was_probe)
            raise
        else:
            self._success()
            return result
