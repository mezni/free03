from unittest.mock import MagicMock

import pytest

from src.application.container import ApplicationContainer
from src.config.settings import (
    ApplicationConfig,
    EmbeddingConfig,
    EnvironmentSettings,
    LoggingConfig,
    Settings,
)


def create_test_settings(
    embedding: EmbeddingConfig | None = None,
) -> Settings:
    return Settings(
        environment=EnvironmentSettings(
            database_url="postgresql://test:test@localhost/test",
        ),
        application=ApplicationConfig(
            name="rag-system",
            environment="test",
        ),
        logging=LoggingConfig(level="INFO"),
        embedding=embedding or EmbeddingConfig(
            provider="local",
            model="local-dev",
            dimensions=8,
        ),
    )


def test_container_creates_document_repository():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(),
    )

    repository = container.document_repository()

    assert repository is not None


def test_container_creates_retrieval_pipeline():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(),
    )

    pipeline = container.retrieval_pipeline()

    assert pipeline is not None


def test_container_creates_evaluation_runner():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(),
    )

    runner = container.retrieval_evaluation_runner()

    assert runner is not None


def test_container_creates_embedding_provider():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(),
    )

    provider = container.embedding_provider()

    assert provider is not None
    assert provider.dimensions == 8


def test_container_reads_embedding_dimensions_from_settings():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(
            EmbeddingConfig(
                provider="local",
                model="local-dev",
                dimensions=16,
            )
        ),
    )

    provider = container.embedding_provider()

    assert provider.dimensions == 16


def test_container_rejects_unknown_embedding_provider():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(
            EmbeddingConfig(
                provider="unknown",
                model="test",
                dimensions=8,
            )
        ),
    )

    with pytest.raises(
        ValueError,
        match="Unsupported embedding provider: unknown",
    ):
        container.embedding_provider()