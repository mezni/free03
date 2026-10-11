"""Deadline-aware execution for latency-bounded operations.

A *timeout* limits one operation; a *deadline* limits the whole workflow. Three
attempts of 10 seconds each, plus backoff delays, can exceed a 30-second
end-to-end budget, so a per-attempt timeout alone is not enough. The helpers here
compute the remaining budget with a monotonic clock and never let a single
attempt's timeout exceed it.

Important limitation: this module does not forcibly stop a synchronous
operation. The operation must honor the timeout it is given. If the underlying
client ignores it, the call can run past the deadline. Enforcement belongs in the
provider SDK's request timeout.
"""

import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class DeadlineExceededError(TimeoutError):
    """The overall operation deadline has expired."""


def remaining_seconds(
    deadline: float,
    *,
    clock: Callable[[], float] = time.monotonic,
) -> float:
    """Return the seconds left before ``deadline``.

    The result is negative once the deadline has passed. A monotonic clock is
    used because it is unaffected by wall-clock adjustments.
    """
    return deadline - clock()


def call_with_deadline(
    operation: Callable[[float], T],
    *,
    deadline: float,
    clock: Callable[[], float] = time.monotonic,
    max_attempt_timeout_seconds: float = 10.0,
) -> T:
    """Call an operation with a timeout bounded by its deadline.

    The operation receives a timeout that is the smaller of the per-attempt
    limit and the remaining budget. If the deadline has already expired, the
    operation is not started and :class:`DeadlineExceededError` is raised.
    """
    remaining = deadline - clock()

    if remaining <= 0:
        raise DeadlineExceededError("Operation deadline expired before the call")

    timeout_seconds = min(
        remaining,
        max_attempt_timeout_seconds,
    )

    return operation(timeout_seconds)
