import pytest

from src.config.settings import EmbeddingConfig
from src.providers.embeddings.factory import (
    EmbeddingProviderFactory,
)
from src.providers.embeddings.local import LocalEmbeddingProvider


def test_factory_creates_local_provider():
    config = EmbeddingConfig(
        provider="local",
        model="local-dev",
        dimensions=8,
    )

    factory = EmbeddingProviderFactory()

    provider = factory.create(config)

    assert isinstance(
        provider,
        LocalEmbeddingProvider,
    )

    assert provider.model_name == "local-dev"
    assert provider.dimensions == 8


def test_factory_rejects_unknown_provider():
    config = EmbeddingConfig(
        provider="does-not-exist",
        model="test",
        dimensions=8,
    )

    factory = EmbeddingProviderFactory()

    with pytest.raises(
        ValueError,
        match="Unsupported embedding provider",
    ):
        factory.create(config)


def test_factory_accepts_uppercase_provider():
    config = EmbeddingConfig(
        provider="LOCAL",
        model="local-dev",
        dimensions=8,
    )

    provider = EmbeddingProviderFactory().create(config)

    assert provider.model_name == "local-dev"


def test_factory_normalizes_padded_provider_name():
    config = EmbeddingConfig(
        provider="  Local  ",
        model="local-dev",
        dimensions=8,
    )

    provider = EmbeddingProviderFactory().create(config)

    assert provider.model_name == "local-dev"


def test_factory_rejects_whitespace_only_provider():
    config = EmbeddingConfig(
        provider="   ",
        model="local-dev",
        dimensions=8,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported embedding provider",
    ):
        EmbeddingProviderFactory().create(config)
