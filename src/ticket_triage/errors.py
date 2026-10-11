from ticket_triage.classification import ClassificationError


class TransientProviderError(ClassificationError):
    """A temporary provider failure that may be retried."""


class PermanentProviderError(ClassificationError):
    """A provider failure that should not be retried unchanged."""


class InvalidModelOutputError(ClassificationError):
    """The model response cannot be used safely."""


class PolicyViolationError(ValueError):
    """The recommendation violates application policy."""


class RoutingProviderError(RuntimeError):
    """Base class for errors raised by an external routing provider."""


class RoutingConfirmedFailure(RoutingProviderError):
    """The provider guarantees the routing operation did not occur.

    Only raise this when the provider's response is trustworthy evidence that
    no side effect was committed. A timeout or connection loss is not evidence
    of failure and must not be reported as this error.
    """


class RoutingOutcomeUnknownError(RoutingProviderError):
    """The external routing operation may have succeeded.

    Used for timeouts, connection loss, and any response the application cannot
    trust as confirmation. The operation must be reconciled, not retried
    blindly.
    """


class RoutingLookupInconclusiveError(RoutingProviderError):
    """A provider lookup cannot determine whether the operation occurred.

    This is distinct from a lookup that definitively finds no matching
    operation. An inconclusive lookup must never be treated as proof that the
    original request was not accepted.
    """


class ApplicationError(RuntimeError):
    """Raised when an application use case cannot be completed."""


class CaseNotFoundError(ApplicationError):
    """Raised when a requested case does not exist."""


class DuplicateCaseError(ApplicationError):
    """Raised when creating a case that already exists."""


class InvalidCaseStateError(ApplicationError):
    """Raised when an operation is not valid for the current case state."""


class ConcurrentUpdateError(ApplicationError):
    """Raised when a conditional write loses a race to another writer."""


class RoutingOperationNotFoundError(ApplicationError):
    """Raised when a requested routing operation does not exist."""
