import pytest
from pydantic import ValidationError

from ticket_triage.config import Settings


def test_defaults_allow_fake_classifier():
    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert settings.database_path == "ticket_triage.db"
    assert settings.openai_api_key is None
    assert settings.openai_model == "gpt-4o-mini"


def test_reads_environment_variables(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("TRIAGE_DATABASE_PATH", "test.db")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    settings = Settings(_env_file=None)

    assert settings.app_env == "test"
    assert settings.database_path == "test.db"
    assert settings.openai_model == "test-model"


def test_rejects_unknown_environment():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, APP_ENV="staging")


def test_rejects_invalid_token_registry():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, TRIAGE_API_TOKENS="{invalid-json")
