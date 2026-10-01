import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pytest

from src.db.repositories.index_versions import IndexVersionRepository
from src.db.repositories.vector_search import VectorSearchRepository
from src.ingestion.context import (
    ChunkEmbedding,
    DocumentChunk,
    DocumentInput,
    DocumentMetadata,
    EmbeddedDocument,
)
from src.models.retrieval import RetrievalFilter, RetrievalQuery
from src.providers.embeddings.local import LocalEmbeddingProvider
from src.services.indexing_service import IndexingService
from src.services.retrieval_service import RetrievalService
from src.services.versioning_service import VersioningService


def _embedded_document(
    source_uri: str,
    content: str,
    dimensions: int = 8,
    *,
    source: str = "filesystem",
) -> EmbeddedDocument:
    metadata = DocumentMetadata(
        source=source,
        source_uri=source_uri,
        file_name="policy.md",
        extension=".md",
        document_type="markdown",
        title="Policy",
        file_size_bytes=100,
        modified_at=datetime.now(UTC),
    )

    document_input = DocumentInput(
        source=source,
        source_uri=source_uri,
        path=Path(source_uri),
    )

    return EmbeddedDocument(
        document=document_input,
        content_hash=hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest(),
        metadata=metadata,
        chunks=[
            DocumentChunk(
                chunk_id=f"{source_uri}#0",
                document=document_input,
                content=content,
                content_hash=hashlib.sha256(
                    content.encode("utf-8")
                ).hexdigest(),
                chunk_index=0,
                start_char=0,
                end_char=len(content),
                metadata=metadata,
            )
        ],
        embeddings=[
            ChunkEmbedding(
                chunk_id=f"{source_uri}#0",
                vector=[0.1] * dimensions,
                model_name="local-deterministic",
                dimensions=dimensions,
            )
        ],
    )


def _retrieval_service(
    database_session,
    dimensions: int = 8,
) -> RetrievalService:
    from src.retrieval.search.vector import VectorSearchStrategy

    embedding_provider = LocalEmbeddingProvider(
        dimensions=dimensions
    )

    return RetrievalService(
        index_version_repository=IndexVersionRepository(
            database_session
        ),
        search_strategy=VectorSearchStrategy(
            repository=VectorSearchRepository(
                database_session
            ),
            embedding_provider=embedding_provider,
        ),
        embedding_provider=embedding_provider,
    )


def _with_active_version(
    database_session,
) -> tuple[IndexingService, VersioningService]:
    indexing = IndexingService(database_session)
    versioning = VersioningService(database_session)

    version = versioning.create_version(
        "local-deterministic",
        8,
    )
    versioning.activate_version(version)
    database_session.commit()

    return indexing, versioning


def test_search_only_returns_chunks_from_active_version(
    database_session,
) -> None:
    indexing = IndexingService(database_session)
    versioning = VersioningService(database_session)

    retired_version = versioning.create_version(
        "local-deterministic",
        8,
    )
    versioning.activate_version(retired_version)
    database_session.commit()

    indexing.add(
        _embedded_document(
            "/tmp/old.md",
            "old information",
        )
    )

    active_version = versioning.create_version(
        "local-deterministic",
        8,
    )
    indexing.add_to_version(
        _embedded_document(
            "/tmp/current.md",
            "current information",
        ),
        active_version.id,
    )
    versioning.activate_version(active_version)
    database_session.commit()

    results = _retrieval_service(
        database_session
    ).search(
        RetrievalQuery(query="current", top_k=5)
    )

    assert results

    assert all(
        result.index_version_id == active_version.id
        for result in results
    )

    assert all(
        "old information" not in result.content
        for result in results
    )


def test_search_filters_by_source(database_session) -> None:
    indexing, _ = _with_active_version(database_session)

    indexing.add(
        _embedded_document(
            "/tmp/billing.md",
            "billing policy information",
            source="billing",
        )
    )
    indexing.add(
        _embedded_document(
            "/tmp/hr.md",
            "hr policy information",
            source="hr",
        )
    )

    document = indexing.documents.get_by_source_uri(
        "/tmp/billing.md"
    )

    assert document is not None

    results = _retrieval_service(
        database_session
    ).search(
        RetrievalQuery(
            query="policy",
            top_k=5,
            filters=RetrievalFilter(
                source="billing",
            ),
        )
    )

    assert results
    assert all(
        result.document_id == document.id
        for result in results
    )


def test_search_filters_by_document_id(
    database_session,
) -> None:
    indexing, _ = _with_active_version(database_session)

    indexing.add(
        _embedded_document(
            "/tmp/billing.md",
            "billing policy information",
            source="billing",
        )
    )
    indexing.add(
        _embedded_document(
            "/tmp/hr.md",
            "hr policy information",
            source="hr",
        )
    )

    document = indexing.documents.get_by_source_uri(
        "/tmp/billing.md"
    )

    assert document is not None

    results = _retrieval_service(
        database_session
    ).search(
        RetrievalQuery(
            query="policy",
            top_k=5,
            filters=RetrievalFilter(
                document_id=document.id,
            ),
        )
    )

    assert results
    assert all(
        result.document_id == document.id
        for result in results
    )


def test_search_without_filters_returns_every_document(
    database_session,
) -> None:
    indexing, _ = _with_active_version(database_session)

    indexing.add(
        _embedded_document(
            "/tmp/billing.md",
            "billing policy information",
            source="billing",
        )
    )
    indexing.add(
        _embedded_document(
            "/tmp/hr.md",
            "hr policy information",
            source="hr",
        )
    )

    billing = indexing.documents.get_by_source_uri(
        "/tmp/billing.md"
    )
    hr = indexing.documents.get_by_source_uri("/tmp/hr.md")

    assert billing is not None
    assert hr is not None

    results = _retrieval_service(
        database_session
    ).search(
        RetrievalQuery(query="policy", top_k=5)
    )

    result_documents = {
        result.document_id
        for result in results
    }

    assert billing.id in result_documents
    assert hr.id in result_documents


def test_search_requires_active_version(
    database_session,
) -> None:
    service = _retrieval_service(database_session)

    with pytest.raises(
        ValueError,
        match="No active index version",
    ):
        service.search(
            RetrievalQuery(query="anything")
        )


def test_search_rejects_query_dimension_mismatch(
    database_session,
) -> None:
    versioning = VersioningService(database_session)

    version = versioning.create_version(
        "local-deterministic",
        8,
    )
    versioning.activate_version(version)
    database_session.commit()

    service = _retrieval_service(
        database_session,
        dimensions=1536,
    )

    with pytest.raises(
        ValueError,
        match="dimensions do not match",
    ):
        service.search(
            RetrievalQuery(query="anything")
        )