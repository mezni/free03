from src.embeddings.local import LocalEmbeddingProvider


def test_local_embedding_provider() -> None:
    provider = LocalEmbeddingProvider(dimensions=8)

    vectors = provider.embed(
        [
            "billing policy",
            "roaming policy",
        ]
    )

    assert len(vectors) == 2
    assert len(vectors[0]) == 8
    assert len(vectors[1]) == 8


def test_embedding_is_deterministic() -> None:
    provider = LocalEmbeddingProvider(dimensions=8)

    first = provider.embed(["billing policy"])
    second = provider.embed(["billing policy"])

    assert first == second


def test_embedding_model_metadata() -> None:
    provider = LocalEmbeddingProvider(dimensions=8)

    assert provider.model_name == "local-deterministic"
    assert provider.dimensions == 8