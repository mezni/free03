import hashlib
from uuid import UUID, uuid4

from src.core.enums import DocumentLifecycleStatus
from src.db.models.chunk import ChunkDB
from src.db.repositories.chunks import ChunkRepository
from src.db.repositories.documents import DocumentRepository
from src.db.repositories.embeddings import EmbeddingRepository
from src.db.repositories.index_versions import IndexVersionRepository
from src.models.document import DocumentCreate
from src.services.index_validation_service import IndexValidationService
from src.services.versioning_service import VersioningService


def _validation_service(
    database_session,
) -> IndexValidationService:
    return IndexValidationService(
        index_version_repository=IndexVersionRepository(database_session),
        chunk_repository=ChunkRepository(database_session),
        embedding_repository=EmbeddingRepository(database_session),
    )


def _build_building_version(
    database_session,
    dimensions: int = 8,
):
    versioning = VersioningService(database_session)
    version = versioning.create_version(
        "local-deterministic",
        dimensions,
    )
    database_session.commit()
    return version


def _add_chunks(
    database_session,
    index_version_id: UUID,
    contents: list[str],
    *,
    declared_dimensions: int = 8,
) -> UUID:
    documents = DocumentRepository(database_session)
    chunks = ChunkRepository(database_session)
    embeddings = EmbeddingRepository(database_session)

    document = documents.create(
        DocumentCreate(
            source="filesystem",
            source_uri=f"/tmp/{uuid4()}.md",
            title="Policy",
            content_hash=hashlib.sha256("".join(contents).encode("utf-8")).hexdigest(),
            status=DocumentLifecycleStatus.ACTIVE,
        )
    )

    for index, content in enumerate(contents):
        chunk = chunks.create(
            document_id=document.id,
            index_version_id=index_version_id,
            chunk_index=index,
            content=content,
            content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            start_char=0,
            end_char=len(content),
        )

        embeddings.create(
            chunk_id=chunk.id,
            model_name="local-deterministic",
            dimensions=declared_dimensions,
            vector=[0.1] * 8,
        )

    return document.id


def test_validates_clean_building_index(
    database_session,
) -> None:
    version = _build_building_version(database_session)

    _add_chunks(
        database_session,
        version.id,
        ["chunk zero", "chunk one"],
    )

    result = _validation_service(database_session).validate(version.id)

    assert result.valid is True
    assert result.document_count == 1
    assert result.chunk_count == 2
    assert result.embedding_count == 2
    assert result.expected_embedding_dimensions == 8
    assert result.invalid_embedding_count == 0
    assert result.duplicate_chunk_count == 0
    assert result.chunks_without_embeddings == 0
    assert result.errors == []


def test_reports_missing_embeddings(
    database_session,
) -> None:
    version = _build_building_version(database_session)

    _add_chunks(
        database_session,
        version.id,
        ["chunk zero", "chunk one"],
    )

    embeddings = EmbeddingRepository(database_session)

    first_embedding = embeddings.get_by_index_version_id(version.id)[0]

    database_session.delete(first_embedding)
    database_session.commit()

    result = _validation_service(database_session).validate(version.id)

    assert result.valid is False
    assert result.chunks_without_embeddings == 1


def test_reports_wrong_embedding_dimensions(
    database_session,
) -> None:
    version = _build_building_version(
        database_session,
        dimensions=8,
    )

    _add_chunks(
        database_session,
        version.id,
        ["chunk"],
        declared_dimensions=1536,
    )

    result = _validation_service(database_session).validate(version.id)

    assert result.valid is False
    assert result.invalid_embedding_count == 1


def test_reports_empty_index(
    database_session,
) -> None:
    version = _build_building_version(database_session)

    result = _validation_service(database_session).validate(version.id)

    assert result.valid is False
    assert result.chunk_count == 0
    assert any("no chunks" in error for error in result.errors)


def test_detects_duplicate_chunk_positions(
    database_session,
) -> None:
    document_id = uuid4()

    chunks = [
        ChunkDB(
            id=uuid4(),
            document_id=document_id,
            chunk_index=0,
        ),
        ChunkDB(
            id=uuid4(),
            document_id=document_id,
            chunk_index=0,
        ),
        ChunkDB(
            id=uuid4(),
            document_id=document_id,
            chunk_index=1,
        ),
    ]

    service = _validation_service(database_session)

    assert service._count_duplicate_chunks(chunks) == 1
