import pytest
from pydantic import ValidationError

from src.config.settings import EmbeddingConfig, get_settings


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


def test_embedding_config_rejects_misspelled_field():
    with pytest.raises(ValidationError):
        EmbeddingConfig.model_validate(
            {
                "provider": "local",
                "model": "local-dev",
                "dimension": 8,
            }
        )


def test_embedding_config_rejects_non_positive_dimensions():
    with pytest.raises(ValidationError):
        EmbeddingConfig(
            provider="local",
            model="local-dev",
            dimensions=0,
        )


def test_embedding_config_rejects_empty_provider():
    with pytest.raises(ValidationError):
        EmbeddingConfig(
            provider="",
            model="local-dev",
            dimensions=8,
        )