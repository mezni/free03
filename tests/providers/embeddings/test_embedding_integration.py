from src.config.settings import EmbeddingConfig
from src.providers.embeddings.factory import (
    EmbeddingProviderFactory,
)


def test_configured_embedding_provider():
    config = EmbeddingConfig(
        provider="local",
        model="local-dev",
        dimensions=8,
    )

    provider = EmbeddingProviderFactory().create(config)

    texts = [
        "billing dispute policy",
        "account security policy",
    ]

    vectors = provider.embed(texts)

    assert len(vectors) == 2
    assert all(len(vector) == 8 for vector in vectors)


def test_configured_provider_supports_query_embedding():
    config = EmbeddingConfig(
        provider="local",
        model="local-dev",
        dimensions=8,
    )

    provider = EmbeddingProviderFactory().create(config)

    vector = provider.embed_query("How do I dispute a bill?")

    assert len(vector) == 8


def test_configured_provider_matches_index_version_dimensions():
    config = EmbeddingConfig(
        provider="local",
        model="local-dev",
        dimensions=8,
    )

    provider = EmbeddingProviderFactory().create(config)

    vectors = provider.embed(
        [
            "billing dispute policy",
            "account security policy",
        ]
    )

    assert provider.dimensions == config.dimensions

    assert all(len(vector) == config.dimensions for vector in vectors)
