class RAGSystemError(Exception):
    """Base application exception."""


class RetrievalError(RAGSystemError):
    """Raised when retrieval fails."""


class GenerationError(RAGSystemError):
    """Raised when LLM generation fails."""


class ConfigurationError(RAGSystemError):
    """Raised when application configuration is invalid."""


class ProviderError(GenerationError):
    """Base class for LLM provider failures.

    Subclasses `GenerationError` so the API layer can map provider
    failures onto the generation status code without registering a
    separate handler for every provider-specific class.
    """


class ProviderTimeoutError(ProviderError):
    """Raised when an external provider times out."""


class ProviderResponseError(ProviderError):
    """Raised when an external provider returns an invalid response.

    Covers client-side rejections (HTTP 4xx), which are deterministic:
    an invalid key, model, or request will fail identically on every
    attempt, so this is never retried.
    """


class TransientProviderError(ProviderResponseError):
    """Raised for provider failures that may succeed on retry.

    HTTP 5xx and connection failures. Retried according to the
    configured retry policy.
    """