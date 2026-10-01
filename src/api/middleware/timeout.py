"""Upper bound on the duration of a whole API request.

`asyncio.wait_for` around `call_next` bounds how long the API will
*wait* for a response. It does not cancel work that has already left the
event loop: a blocking call inside a synchronous endpoint runs on a
thread and keeps running after the client has been given a 504. The
bound is on the client's wait, not on total work done.

That is still worth having, but it should not be mistaken for
cancellation. Real cancellation requires propagating the timeout into
the downstream calls themselves (database `statement_timeout`, provider
HTTP timeouts), which are configured separately.
"""

import asyncio

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.observability.context import get_request_id


class RequestTimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        timeout_seconds: float,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError(
                "timeout_seconds must be greater than zero"
            )

        super().__init__(app)
        self._timeout_seconds = timeout_seconds

    @property
    def timeout_seconds(self) -> float:
        return self._timeout_seconds

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        try:
            return await asyncio.wait_for(
                call_next(request),
                timeout=self._timeout_seconds,
            )
        except TimeoutError:
            # A JSONResponse is returned directly rather than raising
            # HTTPException: this middleware sits above the layer where
            # exception handlers are installed, so a raised exception
            # would bypass them and surface as an unhandled 500.
            return JSONResponse(
                status_code=504,
                content={
                    "error": {
                        "code": "request_timeout",
                        "message": "The request timed out.",
                        "request_id": get_request_id(),
                    }
                },
            )