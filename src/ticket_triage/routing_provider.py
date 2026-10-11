"""Provider-neutral interface for routing tickets to an external system.

The application depends on this small protocol rather than on any specific
ticketing vendor, so the workflow can be tested with a fake and swapped for a
real integration without changing orchestration code.

The interface is intentionally a learning contract, not a complete provider
specification. In particular, ``lookup_by_idempotency_key`` returning ``None``
must mean "no matching operation was found according to the provider's
documented consistency guarantees". A lookup that cannot determine the outcome
must raise ``RoutingLookupInconclusiveError`` instead of returning ``None``.
"""

from enum import StrEnum
from typing import Protocol

from ticket_triage.errors import (
    RoutingConfirmedFailure,
    RoutingLookupInconclusiveError,
)


class RoutingProvider(Protocol):
    """Route tickets and discover whether a prior route call took effect."""

    def route(
        self,
        *,
        ticket_id: str,
        destination: str,
        idempotency_key: str,
    ) -> str:
        """Return the provider's confirmed external reference.

        Raise ``RoutingConfirmedFailure`` only when the provider guarantees the
        operation did not occur. Raise ``RoutingOutcomeUnknownError`` (or let a
        timeout or connection error propagate) when the result cannot be
        confirmed.
        """
        ...

    def lookup_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> str | None:
        """Return a confirmed external reference if found.

        Return ``None`` only when the provider definitively confirms that no
        matching operation exists. Raise ``RoutingLookupInconclusiveError`` when
        the outcome cannot be determined (for example, under eventual
        consistency).
        """
        ...


class RoutingOutcome(StrEnum):
    """How the application should interpret a provider interaction."""

    CONFIRMED_SUCCESS = "confirmed_success"
    CONFIRMED_FAILURE = "confirmed_failure"
    UNKNOWN = "unknown"


def classify_provider_error(error: BaseException) -> RoutingOutcome:
    """Classify a provider error conservatively.

    An operation is only a confirmed failure when the provider raised
    ``RoutingConfirmedFailure``. Everything else—timeouts, connection loss,
    unexpected errors, and errors we do not recognize—remains unknown, because
    the external side effect may already have been committed.
    """
    if isinstance(error, RoutingConfirmedFailure):
        return RoutingOutcome.CONFIRMED_FAILURE
    return RoutingOutcome.UNKNOWN


__all__ = [
    "RoutingLookupInconclusiveError",
    "RoutingOutcome",
    "RoutingProvider",
    "classify_provider_error",
]
