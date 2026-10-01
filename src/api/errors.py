from fastapi import Request
from fastapi.responses import JSONResponse


class RAGAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def register_exception_handlers(app) -> None:

    @app.exception_handler(RAGAPIError)
    async def rag_api_error_handler(
        request: Request,
        exc: RAGAPIError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
            },
        )