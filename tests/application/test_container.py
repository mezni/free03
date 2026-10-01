from unittest.mock import MagicMock

import pytest

from src.application.container import ApplicationContainer
from src.config.settings import (
    ApplicationConfig,
    EmbeddingConfig,
    EnvironmentSettings,
    LLMConfig,
    LoggingConfig,
    Settings,
)


def create_test_settings(
    embedding: EmbeddingConfig | None = None,
    openrouter_api_key: str | None = None,
) -> Settings:
    return Settings(
        environment=EnvironmentSettings(
            database_url="postgresql://test:test@localhost/test",
            openrouter_api_key=openrouter_api_key,
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
        llm=LLMConfig(
            provider="openrouter",
            model="openai/gpt-oss-20b:free",
            temperature=0.0,
            max_tokens=1000,
            timeout_seconds=60,
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
    assert provider.model_name == "local-dev"
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

def test_container_creates_llm_provider():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(
            openrouter_api_key="test-key"
        ),
    )

    provider = container.llm_provider()

    assert provider.model_name == "openai/gpt-oss-20b:free"


def test_container_requires_llm_api_key():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(),
    )

    with pytest.raises(
        ValueError,
        match="OPENROUTER_API_KEY is required",
    ):
        container.llm_provider()


def test_container_creates_rag_service():
    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(
            openrouter_api_key="test-key"
        ),
    )

    rag_service = container.rag_service()

    assert rag_service is not None


def test_container_creates_rag_evaluation_service():
    from src.evaluation.answer.semantic import (
        SimpleAnswerEvaluator,
    )
    from src.evaluation.citation.evaluator import (
        CitationEvaluator,
    )
    from src.evaluation.grounding.evaluator import (
        GroundingEvaluator,
    )
    from src.services.rag_evaluation_service import (
        RAGEvaluationService,
    )

    session = MagicMock()

    container = ApplicationContainer(
        session=session,
        settings=create_test_settings(
            openrouter_api_key="test-key"
        ),
    )

    service = container.rag_evaluation_service()

    assert isinstance(service, RAGEvaluationService)
    assert isinstance(
        service._answer_evaluator,
        SimpleAnswerEvaluator,
    )
    assert isinstance(
        service._citation_evaluator,
        CitationEvaluator,
    )
    assert isinstance(
        service._grounding_evaluator,
        GroundingEvaluator,
    )
