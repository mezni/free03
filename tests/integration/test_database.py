from src.core.enums import DocumentLifecycleStatus
from src.db.repositories.documents import DocumentRepository
from src.models.document import DocumentCreate


def test_create_and_get_document(database_session):
    repository = DocumentRepository(database_session)

    document = repository.create(
        DocumentCreate(
            source="filesystem",
            source_uri="data/raw/billing/sample.md",
            title="Billing Policy",
            content_hash="a" * 64,
        )
    )

    database_session.commit()

    stored_document = repository.get_by_id(document.id)

    assert stored_document is not None
    assert stored_document.id == document.id
    assert stored_document.title == "Billing Policy"
    assert stored_document.source == "filesystem"
    assert stored_document.status == DocumentLifecycleStatus.PENDING.value


def test_find_document_by_source_uri(database_session):
    repository = DocumentRepository(database_session)

    repository.create(
        DocumentCreate(
            source="filesystem",
            source_uri="data/raw/roaming/roaming.md",
            title="Roaming Policy",
            content_hash="b" * 64,
        )
    )

    database_session.commit()

    document = repository.get_by_source_uri("data/raw/roaming/roaming.md")

    assert document is not None
    assert document.title == "Roaming Policy"


def test_find_document_by_content_hash(database_session):
    repository = DocumentRepository(database_session)

    content_hash = "c" * 64

    repository.create(
        DocumentCreate(
            source="filesystem",
            source_uri="data/raw/billing/hash-test.md",
            title="Hash Test",
            content_hash=content_hash,
        )
    )

    database_session.commit()

    document = repository.get_by_content_hash(content_hash)

    assert document is not None
    assert document.source_uri == "data/raw/billing/hash-test.md"


def test_document_repository_returns_domain_model(database_session):
    repository = DocumentRepository(database_session)

    data = DocumentCreate(
        source="filesystem",
        source_uri="data/raw/billing/domain.md",
        title="Billing Policy",
        content_hash="d" * 64,
    )

    database_document = repository.create(data)

    database_session.commit()

    document = repository.get_domain_by_id(database_document.id)

    assert document is not None
    assert document.source == "filesystem"
    assert document.title == "Billing Policy"
    assert document.content_hash == "d" * 64
