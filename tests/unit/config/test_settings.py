import pytest
from pydantic import ValidationError

from src.config.settings import (
    EmbeddingConfig,
    FinOpsConfig,
    ModelPricing,
    get_settings,
)


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


def test_settings_load_finops_config():
    settings = get_settings()

    assert settings.finops.currency == "USD"

    pricing = settings.finops.pricing["openrouter"]

    assert (
        pricing["openai/gpt-oss-20b:free"].input_per_1m_tokens
        == 0.0
    )


def test_settings_load_quality_gate_config():
    settings = get_settings()

    gate = settings.evaluation.quality_gate

    assert gate.min_answer_relevance == 0.60
    assert gate.min_citation_precision == 0.80
    assert gate.min_citation_recall == 0.80
    assert gate.min_grounding == 0.80


def test_finops_config_rejects_negative_price():
    with pytest.raises(ValidationError):
        FinOpsConfig(
            currency="USD",
            pricing={
                "openrouter": {
                    "test-model": ModelPricing(
                        input_per_1m_tokens=-1.0,
                        output_per_1m_tokens=1.0,
                    )
                }
            },
        )


def test_finops_config_rejects_unknown_price_field():
    with pytest.raises(ValidationError):
        FinOpsConfig(
            currency="USD",
            pricing={
                "openrouter": {
                    "test-model": {
                        "input_per_1m_tokens": 1.0,
                        "output_per_1m_tokens": 2.0,
                        "per_request": 0.01,
                    }
                }
            },
        )


def test_finops_config_rejects_bad_currency_length():
    with pytest.raises(ValidationError):
        FinOpsConfig(
            currency="DOLLARS",
            pricing={},
        )