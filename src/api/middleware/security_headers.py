from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Baseline hardening headers.

    Transport-level concerns (TLS, request size, rate limits,
    connection limits) belong to the reverse proxy in front of this
    service, not here.
    """

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"

        return response
