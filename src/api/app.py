import logging

from fastapi import FastAPI, Request

from src.api.errors import register_exception_handlers
from src.api.lifespan import lifespan
from src.api.middleware.security_headers import (
    SecurityHeadersMiddleware,
)
from src.api.routes.documents import router as documents_router
from src.api.routes.health import router as health_router
from src.api.routes.metrics import router as metrics_router
from src.api.routes.rag import router as rag_router
from src.api.routes.ingestion import router as ingestion_router
from src.config.settings import get_settings
from src.observability.context import create_request_id
from src.observability.logging import configure_logging
from src.observability.timer import Timer

logger = logging.getLogger("rag-system.api")


def create_app() -> FastAPI:
    settings = get_settings()

    configure_logging(settings.logging.level)

    app = FastAPI(
        title="rag-system",
        description=("Production-oriented Retrieval-Augmented Generation API"),
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(SecurityHeadersMiddleware)

    @app.middleware("http")
    async def observability_middleware(
        request: Request,
        call_next,
    ):
        request_id = create_request_id()

        with Timer() as timer:
            response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "HTTP request completed",
            extra={
                "event": "http.request.completed",
                "duration_ms": timer.duration_ms,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
            },
        )

        return response

    app.include_router(health_router)
    app.include_router(documents_router)
    app.include_router(rag_router)
    app.include_router(metrics_router)
    app.include_router(ingestion_router)

    register_exception_handlers(app)

    return app


app = create_app()
