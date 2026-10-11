from ticket_triage.classification import ClassificationError


class TransientProviderError(ClassificationError):
    """A temporary provider failure that may be retried."""


class PermanentProviderError(ClassificationError):
    """A provider failure that should not be retried unchanged."""


class InvalidModelOutputError(ClassificationError):
    """The model response cannot be used safely."""


class PolicyViolationError(ValueError):
    """The recommendation violates application policy."""


class RoutingOutcomeUnknownError(RuntimeError):
    """The external routing operation may have succeeded."""


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
