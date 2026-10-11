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