from unittest.mock import MagicMock

from src.application.container import ApplicationContainer


def test_container_creates_document_repository():
    session = MagicMock()

    container = ApplicationContainer(session)

    repository = container.document_repository()

    assert repository is not None


def test_container_creates_retrieval_pipeline():
    session = MagicMock()

    container = ApplicationContainer(session)

    pipeline = container.retrieval_pipeline()

    assert pipeline is not None


def test_container_creates_evaluation_runner():
    session = MagicMock()

    container = ApplicationContainer(session)

    runner = container.retrieval_evaluation_runner()

    assert runner is not None