import logging
from collections.abc import Awaitable, Callable
from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from src.core.exceptions import (
    ConfigurationError,
    GenerationError,
    ProviderTimeoutError,
    RetrievalError,
)
from src.observability.context import get_request_id

logger = logging.getLogger("rag-system.api")

ExceptionHandler = Callable[
    [Request, Exception],
    Response | Awaitable[Response],
]


class RAGAPIError(Exception):
    """Explicitly raised API failure with a chosen status code."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def _error(
    message: str,
    status_code: int,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": message,
            "request_id": get_request_id(),
        },
    )


async def provider_timeout_handler(
    request,
    exc: ProviderTimeoutError,
) -> JSONResponse:
    logger.warning(
        "Upstream provider timed out",
        extra={
            "event": "provider.timeout",
            "error_type": type(exc).__name__,
        },
    )

    return _error(
        "The upstream service timed out.",
        504,
    )


async def retrieval_error_handler(
    request,
    exc: RetrievalError,
) -> JSONResponse:
    logger.warning(
        "Retrieval failed",
        extra={
            "event": "retrieval.failed",
            "error_type": type(exc).__name__,
        },
    )

    return _error(
        "Retrieval service is temporarily unavailable.",
        503,
    )


async def generation_error_handler(
    request,
    exc: GenerationError,
) -> JSONResponse:
    logger.warning(
        "Generation failed",
        extra={
            "event": "generation.failed",
            "error_type": type(exc).__name__,
        },
    )

    return _error(
        "Answer generation is temporarily unavailable.",
        502,
    )


async def configuration_error_handler(
    request,
    exc: ConfigurationError,
) -> JSONResponse:
    logger.error(
        "Configuration invalid",
        extra={
            "event": "configuration.invalid",
            "error_type": type(exc).__name__,
        },
    )

    return _error(
        "The service is misconfigured.",
        500,
    )


async def rag_api_error_handler(
    request,
    exc: RAGAPIError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "request_id": get_request_id(),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    # Each handler is bound to a specific exception type, which
    # Starlette's signature types as `Exception`. Registration is
    # wrapped in a helper so the cast happens in one place.
    def register(
        exception_type: type[Exception],
        handler: Callable[..., Awaitable[Response]],
    ) -> None:
        app.add_exception_handler(
            exception_type,
            cast(ExceptionHandler, handler),
        )

    register(RAGAPIError, rag_api_error_handler)
    register(ProviderTimeoutError, provider_timeout_handler)
    register(RetrievalError, retrieval_error_handler)
    register(GenerationError, generation_error_handler)
    register(ConfigurationError, configuration_error_handler)
