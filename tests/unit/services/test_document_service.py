from src.core.enums import DocumentLifecycleStatus
from src.models.document import DocumentCreate
from src.services.document_service import DocumentService


def test_create_document(database_session):
    service = DocumentService(database_session)

    data = DocumentCreate(
        source="filesystem",
        source_uri="data/raw/billing/service-test.md",
        title="Billing Policy",
        content_hash="e" * 64,
    )

    document = service.create_document(data)

    assert document.id is not None
    assert document.source == "filesystem"
    assert document.title == "Billing Policy"
    assert document.status == DocumentLifecycleStatus.PENDING


def test_get_document(database_session):
    service = DocumentService(database_session)

    data = DocumentCreate(
        source="filesystem",
        source_uri="data/raw/billing/get-test.md",
        title="Billing Policy",
        content_hash="f" * 64,
    )

    created = service.create_document(data)

    result = service.get_document(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.source_uri == data.source_uri


def test_delete_document(database_session):
    service = DocumentService(database_session)

    data = DocumentCreate(
        source="filesystem",
        source_uri="data/raw/billing/delete-test.md",
        content_hash="b" * 64,
    )

    created = service.create_document(data)

    deleted = service.delete_document(created.id)

    assert deleted is True
    assert service.get_document(created.id) is None
