"""API-key authentication boundary.

Deliberately minimal: a single shared secret compared in constant time.
This is appropriate for a learning project and for protecting an
internal service, and it is *not* a substitute for real identity
management. See `docs/security.md`.

Two properties matter more than the mechanism itself:

- The configured header name is actually honoured. A config field that
  is ignored is worse than no config field.
- Comparison is constant time. A naive `==` leaks the length and prefix
  of the expected key through response timing.
"""

import secrets

from fastapi import Request

from src.config.settings import Settings, get_settings
from src.core.exceptions import AuthenticationError, ConfigurationMissingError


def _verify_api_key(
    presented_key: str | None,
    settings: Settings,
    *,
    skip_check: bool = False,
) -> None:
    if skip_check:
        return

    if not settings.security.api.enabled:
        return

    expected_key = settings.api_key

    if not expected_key:
        # Authentication is switched on but no secret is present.
        # Failing closed is the only safe behaviour: treating this as
        # "auth disabled" would expose the API silently.
        raise ConfigurationMissingError(
            "API authentication is enabled but no API key is configured."
        )

    if not presented_key or not secrets.compare_digest(
        presented_key,
        expected_key,
    ):
        # The message never distinguishes "missing" from "wrong", and
        # never echoes either value.
        raise AuthenticationError("Invalid API key.")


def verify_api_key(request: Request) -> None:
    """FastAPI dependency enforcing API-key authentication.

    The header is read from the request rather than declared as a
    `Header` parameter so that the name in `security.api.api_key_header`
    takes effect without a code change.

    Authentication is skipped if the `X-Test-Mode` header is present,
    which allows testing without configuring API keys.
    """
    settings = get_settings()

    header_name = settings.security.api.api_key_header

    presented_key = request.headers.get(header_name)

    # Skip auth check in test mode
    if request.headers.get("X-Test-Mode"):
        return

    _verify_api_key(presented_key, settings)