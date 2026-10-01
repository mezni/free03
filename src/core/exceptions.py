class RAGSystemError(Exception):
    """Base application exception.

    `code` is the stable, machine-readable identifier returned to API
    clients. It is a class attribute so that handlers can branch on it
    without importing every concrete type, and so that the value is
    fixed at import time.
    """

    code = "rag_system_error"


class RetrievalError(RAGSystemError):
    """Raised when retrieval fails."""

    code = "retrieval_error"


class GenerationError(RAGSystemError):
    """Raised when LLM generation fails."""

    code = "generation_error"


class ConfigurationError(RAGSystemError):
    """Raised when application configuration is invalid."""

    code = "configuration_error"


class ProviderError(GenerationError):
    """Base class for LLM provider failures.

    Subclasses `GenerationError` so the API layer can map provider
    failures onto the generation status code without registering a
    separate handler for every provider-specific class.
    """

    code = "provider_error"


class ProviderTimeoutError(ProviderError):
    """Raised when an external provider times out."""

    code = "provider_timeout"


class ProviderResponseError(ProviderError):
    """Raised when an external provider returns an invalid response.

    Covers client-side rejections (HTTP 4xx), which are deterministic:
    an invalid key, model, or request will fail identically on every
    attempt, so this is never retried.
    """

    code = "provider_response_error"


class TransientProviderError(ProviderResponseError):
    """Raised for provider failures that may succeed on retry.

    HTTP 5xx and connection failures. Retried according to the
    configured retry policy.
    """

    code = "provider_transient_error"


class RateLimitError(RAGSystemError):
    """Raised when a client exceeds its configured request budget."""

    code = "rate_limit_exceeded"


class AuthenticationError(RAGSystemError):
    """Raised when a request fails authentication.

    The message must never echo the presented credential or the
    expected value.
    """

    code = "authentication_error"


class CircuitOpenError(RAGSystemError):
    """Raised when a provider circuit is open.

    Defined here rather than in `src.providers.circuit_breaker` so that
    a single class is caught by the API exception handler. A second,
    identically named class in the provider module would be a distinct
    type and would never match.
    """

    code = "provider_unavailable"


class ConfigurationMissingError(ConfigurationError):
    """Raised when a required secret or setting is absent.

    Distinct from a malformed configuration: the application is
    correctly formed but cannot run as deployed.
    """

    code = "configuration_missing"