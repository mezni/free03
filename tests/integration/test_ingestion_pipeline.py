from pathlib import Path

from src.db.models.chunk import ChunkDB
from src.db.models.document import DocumentDB
from src.db.models.embedding import EmbeddingDB
from src.ingestion.factory import create_filesystem_ingestion_pipeline


def test_ingestion_pipeline_end_to_end(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    document_path = raw / "billing-policy.md"

    document_path.write_text(
        "# Billing Policy\n\n"
        "Customers are billed according to their active service plan.\n\n"
        "Billing information must be reviewed when a customer "
        "changes their plan.\n",
        encoding="utf-8",
    )

    pipeline = create_filesystem_ingestion_pipeline(
        session=database_session,
        input_dir=raw,
        processed_dir=tmp_path / "processed",
    )

    results = pipeline.run()

    assert results.run_id is not None
    assert results.discovered_count == 1
    assert results.processed_count == 1
    assert results.skipped_count == 0
    assert results.failed_count == 0
    assert len(results.document_ids) == 1

    document = (
        database_session.query(DocumentDB).filter(DocumentDB.source_uri == str(document_path)).one()
    )

    chunks = database_session.query(ChunkDB).filter(ChunkDB.document_id == document.id).all()

    embeddings = (
        database_session.query(EmbeddingDB)
        .join(
            ChunkDB,
            EmbeddingDB.chunk_id == ChunkDB.id,
        )
        .filter(ChunkDB.document_id == document.id)
        .all()
    )

    assert document.title == "Billing Policy"
    assert len(chunks) > 0
    assert len(embeddings) == len(chunks)


def test_ingestion_skips_unchanged_document(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    document_path = raw / "billing-policy.md"
    content = "# Billing Policy\n\nCustomers are billed according to their active service plan.\n"

    document_path.write_text(content, encoding="utf-8")

    pipeline = create_filesystem_ingestion_pipeline(
        session=database_session,
        input_dir=raw,
        processed_dir=tmp_path / "processed",
    )

    first_result = pipeline.run()

    assert first_result.processed_count == 1

    document_path.write_text(content, encoding="utf-8")

    second_result = pipeline.run()

    assert second_result.discovered_count == 1
    assert second_result.processed_count == 0
    assert second_result.skipped_count == 1
    assert document_path.exists()

    documents = (
        database_session.query(DocumentDB).filter(DocumentDB.source_uri == str(document_path)).all()
    )

    assert len(documents) == 1


def test_modified_document_is_reindexed(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    document_path = raw / "billing-policy.md"

    document_path.write_text(
        "# Billing Policy\n\nOriginal billing policy.\n",
        encoding="utf-8",
    )

    pipeline = create_filesystem_ingestion_pipeline(
        session=database_session,
        input_dir=raw,
        processed_dir=tmp_path / "processed",
    )

    first_result = pipeline.run()

    assert first_result.discovered_count == 1
    assert first_result.processed_count == 1

    document = (
        database_session.query(DocumentDB).filter(DocumentDB.source_uri == str(document_path)).one()
    )

    original_hash = document.content_hash

    original_chunks = (
        database_session.query(ChunkDB).filter(ChunkDB.document_id == document.id).all()
    )

    assert len(original_chunks) > 0

    document_path.write_text(
        "# Billing Policy\n\nUpdated billing policy with new information.\n",
        encoding="utf-8",
    )

    second_result = pipeline.run()

    assert second_result.discovered_count == 1
    assert second_result.processed_count == 1
    assert len(second_result.document_ids) == 1

    database_session.refresh(document)

    assert document.content_hash != original_hash

    updated_chunks = (
        database_session.query(ChunkDB).filter(ChunkDB.document_id == document.id).all()
    )

    assert len(updated_chunks) > 0


def test_indexing_service_removes_document_from_active_index(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    document_path = raw / "policy.md"

    document_path.write_text(
        "# Test Policy\n\nTest content.",
        encoding="utf-8",
    )

    pipeline = create_filesystem_ingestion_pipeline(
        session=database_session,
        input_dir=raw,
        processed_dir=tmp_path / "processed",
    )

    pipeline.run()

    document = (
        database_session.query(DocumentDB).filter(DocumentDB.source_uri == str(document_path)).one()
    )

    from src.services.indexing_service import IndexingService

    service = IndexingService(database_session)

    service.delete(document.id)

    assert database_session.query(ChunkDB).filter(ChunkDB.document_id == document.id).count() == 0

    assert database_session.query(DocumentDB).filter(DocumentDB.id == document.id).one() is not None
