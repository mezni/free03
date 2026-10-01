from uuid import UUID

from src.db.models.index_version import IndexVersionDB
from src.db.repositories.vector_search import VectorSearchRepository
from src.models.retrieval import RetrievalFilter
from src.services.indexing_service import IndexingService
from src.services.versioning_service import VersioningService


def _active_index(
    database_session,
    embedded_document_factory,
) -> tuple[IndexVersionDB, UUID, UUID]:
    indexing = IndexingService(database_session)
    versioning = VersioningService(database_session)

    version = versioning.create_version(
        "local-deterministic",
        8,
    )
    versioning.activate_version(version)
    database_session.commit()

    billing_id = indexing.add(
        embedded_document_factory(
            "/tmp/billing.md",
            "billing policy information",
            source="billing",
        )
    )

    hr_id = indexing.add(
        embedded_document_factory(
            "/tmp/hr.md",
            "hr policy information",
            source="hr",
        )
    )

    return (
        version,
        billing_id,
        hr_id,
    )


def test_search_filters_by_source_in_sql(
    database_session,
    embedded_document_factory,
) -> None:
    version, billing_id, hr_id = _active_index(
        database_session,
        embedded_document_factory,
    )

    repository = VectorSearchRepository(database_session)

    billing_rows = repository.search(
        query_vector=[0.1] * 8,
        index_version_id=version.id,
        top_k=5,
        filters=RetrievalFilter(source="billing"),
    )

    assert billing_rows
    assert all(
        chunk.document_id == billing_id
        for chunk, _ in billing_rows
    )
    assert all(
        chunk.index_version_id == version.id
        for chunk, _ in billing_rows
    )

    hr_rows = repository.search(
        query_vector=[0.1] * 8,
        index_version_id=version.id,
        top_k=5,
        filters=RetrievalFilter(source="hr"),
    )

    assert hr_rows
    assert all(
        chunk.document_id == hr_id
        for chunk, _ in hr_rows
    )
    assert all(
        chunk.index_version_id == version.id
        for chunk, _ in hr_rows
    )


def test_search_filters_by_document_id_in_sql(
    database_session,
    embedded_document_factory,
) -> None:
    version, billing_id, hr_id = _active_index(
        database_session,
        embedded_document_factory,
    )

    repository = VectorSearchRepository(database_session)

    rows = repository.search(
        query_vector=[0.1] * 8,
        index_version_id=version.id,
        top_k=5,
        filters=RetrievalFilter(document_id=billing_id),
    )

    assert rows
    assert all(
        chunk.document_id == billing_id
        for chunk, _ in rows
    )
    assert all(
        chunk.index_version_id == version.id
        for chunk, _ in rows
    )
    assert all(
        chunk.document_id != hr_id
        for chunk, _ in rows
    )