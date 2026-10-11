"""Authentication and role-based authorization for the API."""

import json
from dataclasses import dataclass
from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ticket_triage.config import get_settings


@dataclass(frozen=True)
class Principal:
    """Identity and roles of the authenticated caller."""

    subject: str
    roles: frozenset[str]


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> Principal:
    """Authenticate a bearer token against the configured local registry."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Valid authentication credentials are required.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    registry = _load_token_registry()
    entry = registry.get(credentials.credentials)
    if entry is None:
        raise unauthorized
    return Principal(
        subject=entry["subject"],
        roles=frozenset(entry["roles"]),
    )


def require_roles(*roles: str) -> Callable[..., Principal]:
    """Build a dependency that requires at least one of the given roles."""

    def dependency(
        principal: Principal = Depends(get_current_principal),
    ) -> Principal:
        if principal.roles.isdisjoint(roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this operation.",
            )
        return principal

    return dependency


def _load_token_registry() -> dict[str, dict]:
    try:
        registry = json.loads(get_settings().api_tokens_json)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The token registry is misconfigured.",
        )
    if not isinstance(registry, dict):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The token registry is misconfigured.",
        )
    return registry