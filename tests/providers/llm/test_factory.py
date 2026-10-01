import pytest

from src.config.settings import LLMConfig
from src.providers.llm.factory import LLMProviderFactory
from src.providers.llm.openrouter import OpenRouterProvider


def make_config(**overrides) -> LLMConfig:
    kwargs = {
        "provider": "openrouter",
        "model": "openai/gpt-oss-20b:free",
        "temperature": 0.0,
        "max_tokens": 1000,
    }
    kwargs.update(overrides)

    return LLMConfig(**kwargs)


def test_factory_creates_openrouter_provider():
    provider = LLMProviderFactory().create(
        config=make_config(),
        api_key="test-key",
    )

    assert isinstance(
        provider,
        OpenRouterProvider,
    )

    assert provider.model_name == "openai/gpt-oss-20b:free"


def test_factory_accepts_uppercase_provider():
    provider = LLMProviderFactory().create(
        config=make_config(provider="OpenRouter"),
        api_key="test-key",
    )

    assert isinstance(
        provider,
        OpenRouterProvider,
    )


def test_factory_requires_api_key():
    with pytest.raises(
        ValueError,
        match="OPENROUTER_API_KEY is required",
    ):
        LLMProviderFactory().create(
            config=make_config(),
            api_key=None,
        )


def test_factory_rejects_empty_api_key():
    with pytest.raises(
        ValueError,
        match="OPENROUTER_API_KEY is required",
    ):
        LLMProviderFactory().create(
            config=make_config(),
            api_key="",
        )


def test_factory_rejects_unknown_provider():
    with pytest.raises(
        ValueError,
        match="Unsupported LLM provider",
    ):
        LLMProviderFactory().create(
            config=make_config(provider="does-not-exist"),
            api_key="test-key",
        )


def test_factory_does_not_require_api_key_for_unknown_provider():
    """
    Provider selection happens before key validation, so an unknown
    provider reports the unsupported name rather than a missing key.
    """

    with pytest.raises(
        ValueError,
        match="Unsupported LLM provider",
    ):
        LLMProviderFactory().create(
            config=make_config(provider="does-not-exist"),
            api_key=None,
        )