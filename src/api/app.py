from fastapi import FastAPI

from src.api.errors import register_exception_handlers
from src.api.routes.health import router as health_router
from src.api.routes.rag import router as rag_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="rag-system",
        description="Production-oriented RAG API",
        version="1.0.0",
    )

    app.include_router(
        health_router,
    )

    app.include_router(
        rag_router,
    )

    register_exception_handlers(app)

    return app


app = create_app()