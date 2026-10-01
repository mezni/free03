from src.core.enums import DocumentLifecycleStatus
from src.db.repositories.documents import DocumentRepository
from src.models.document import DocumentCreate


def test_document_can_transition_to_processing(database_session):
    repository = DocumentRepository(database_session)

    document = repository.create(
        DocumentCreate(
            source="filesystem",
            source_uri="data/raw/test.md",
            title="Test",
            content_hash="a" * 64,
            status=DocumentLifecycleStatus.PROCESSING,
        )
    )

    database_session.commit()

    assert document.status == DocumentLifecycleStatus.PROCESSING.value


def test_document_can_become_active(database_session):
    repository = DocumentRepository(database_session)

    document = repository.create(
        DocumentCreate(
            source="filesystem",
            source_uri="data/raw/test-active.md",
            title="Test",
            content_hash="b" * 64,
            status=DocumentLifecycleStatus.PROCESSING,
        )
    )

    database_session.commit()

    from src.services.document_service import DocumentService

    service = DocumentService(database_session)

    result = service.set_active(document.id)

    assert result is not None
    assert result.status == DocumentLifecycleStatus.ACTIVE
