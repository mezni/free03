from triage_ai.config import settings


def test_application_name():
    assert settings.app_name == "triage-ai"


def test_environment():
    assert settings.environment == "development"