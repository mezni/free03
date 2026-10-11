from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from ticket_triage.auth import (
    Principal,
    get_current_principal,
    require_roles,
)
from ticket_triage.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_require_roles_returns_principal_for_authorized_role():
    dependency = require_roles("submitter", "admin")

    principal = dependency(
        Principal(subject="dev-user", roles=frozenset({"submitter"}))
    )

    assert principal.subject == "dev-user"


def test_require_roles_forbids_missing_role():
    dependency = require_roles("reviewer")

    with pytest.raises(HTTPException) as exc_info:
        dependency(
            Principal(subject="dev-user", roles=frozenset({"submitter"}))
        )

    assert exc_info.value.status_code == 403


def test_missing_credentials_returns_401():
    with pytest.raises(HTTPException) as exc_info:
        get_current_principal(None)

    assert exc_info.value.status_code == 401


def test_unknown_token_returns_401(monkeypatch):
    monkeypatch.setenv(
        "TRIAGE_API_TOKENS",
        '{"dev-review-token":{"subject":"reviewer-1","roles":["reviewer"]}}',
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_principal(
            SimpleNamespace(credentials="dev-submit-token")
        )

    assert exc_info.value.status_code == 401


def test_known_token_returns_principal(monkeypatch):
    monkeypatch.setenv(
        "TRIAGE_API_TOKENS",
        '{"dev-review-token":{"subject":"reviewer-1","roles":["reviewer"]}}',
    )

    principal = get_current_principal(
        SimpleNamespace(credentials="dev-review-token")
    )

    assert principal.subject == "reviewer-1"
    assert principal.roles == frozenset({"reviewer"})