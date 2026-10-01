from pathlib import Path

from sqlalchemy import delete

from src.db.models.index_version import IndexVersionDB
from src.ingestion.factory import create_filesystem_ingestion_pipeline


def test_success_finalizes_source(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    document_path = raw / "policy.md"
    document_path.write_text(
        "# Billing Policy\n\nBilling content.\n",
        encoding="utf-8",
    )

    processed = tmp_path / "processed"

    pipeline = create_filesystem_ingestion_pipeline(
        session=database_session,
        input_dir=raw,
        processed_dir=processed,
        archive_flag=True,
    )

    result = pipeline.run()

    assert result.processed_count == 1
    assert result.failed_count == 0
    assert not document_path.exists()
    assert (processed / "policy.md").exists()


def test_failure_keeps_source_in_raw(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    document_path = raw / "policy.md"
    document_path.write_text(
        "# Billing Policy\n\nBilling content.\n",
        encoding="utf-8",
    )

    database_session.execute(delete(IndexVersionDB))
    database_session.commit()

    pipeline = create_filesystem_ingestion_pipeline(
        session=database_session,
        input_dir=raw,
        processed_dir=tmp_path / "processed",
        archive_flag=True,
    )

    result = pipeline.run()

    assert result.failed_count == 1
    assert document_path.exists()


def test_skipped_keeps_source_in_raw(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    document_path = raw / "policy.md"
    content = "# Billing Policy\n\nBilling content.\n"

    document_path.write_text(content, encoding="utf-8")

    processed = tmp_path / "processed"

    pipeline = create_filesystem_ingestion_pipeline(
        session=database_session,
        input_dir=raw,
        processed_dir=processed,
        archive_flag=True,
    )

    first_result = pipeline.run()

    assert first_result.processed_count == 1
    assert not document_path.exists()
    assert (processed / "policy.md").exists()

    document_path.write_text(content, encoding="utf-8")

    second_result = pipeline.run()

    assert second_result.skipped_count == 1
    assert document_path.exists()
    assert (processed / "policy.md").exists()
