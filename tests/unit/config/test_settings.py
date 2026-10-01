from src.config.settings import get_settings


def test_settings_load():
    settings = get_settings()

    assert settings.application_name == "rag-system"
    assert settings.environment_name == "dev"
    assert settings.database_url


def test_settings_load_embedding_config():
    settings = get_settings()

    assert settings.embedding.provider == "local"
    assert settings.embedding.model == "local-dev"
    assert settings.embedding.dimensions == 8