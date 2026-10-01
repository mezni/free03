import pytest

from src.providers.embeddings.base import EmbeddingProvider
from src.providers.embeddings.local import LocalEmbeddingProvider


@pytest.fixture
def provider() -> EmbeddingProvider:
    return LocalEmbeddingProvider(
        dimensions=8,
        model_name="local-dev",
    )


def test_provider_exposes_model_name(provider):
    assert provider.model_name == "local-dev"


def test_provider_exposes_dimensions(provider):
    assert provider.dimensions == 8


def test_embed_returns_one_vector_per_text(provider):
    texts = [
        "first document",
        "second document",
        "third document",
    ]

    vectors = provider.embed(texts)

    assert len(vectors) == len(texts)

    for vector in vectors:
        assert len(vector) == provider.dimensions


def test_embed_query_returns_correct_dimensions(provider):
    vector = provider.embed_query("What is the refund policy?")

    assert len(vector) == provider.dimensions


def test_embed_empty_list_returns_empty_list(provider):
    assert provider.embed([]) == []


def test_all_embeddings_have_configured_dimension(provider):
    texts = [
        "billing policy",
        "account security",
        "refund policy",
    ]

    vectors = provider.embed(texts)

    assert all(len(vector) == provider.dimensions for vector in vectors)


def test_embed_query_matches_embed_for_same_text(provider):
    text = "What is the refund policy?"

    assert provider.embed_query(text) == provider.embed([text])[0]
