from pathlib import Path

from src.ingestion.stages.finalizer import FileFinalizer


def test_archive_moves_source_to_processed(
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    source = raw / "document.md"
    source.write_text("# Hello", encoding="utf-8")

    processed = tmp_path / "processed"

    FileFinalizer(
        processed_dir=processed,
        archive_flag=True,
    ).finalize(source)

    assert not source.exists()
    assert (processed / "document.md").exists()


def test_delete_mode_removes_source(
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    source = raw / "document.md"
    source.write_text("# Hello", encoding="utf-8")

    FileFinalizer(
        processed_dir=tmp_path / "processed",
        archive_flag=False,
    ).finalize(source)

    assert not source.exists()


def test_archive_collision_gets_unique_destination(
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()

    processed = tmp_path / "processed"
    processed.mkdir()

    (processed / "document.md").write_text(
        "# Existing",
        encoding="utf-8",
    )

    source = raw / "document.md"
    source.write_text("# New", encoding="utf-8")

    FileFinalizer(
        processed_dir=processed,
        archive_flag=True,
    ).finalize(source)

    assert not source.exists()
    assert (processed / "document.md").read_text() == "# Existing"
    assert (processed / "document_1.md").read_text() == "# New"


def test_finalize_missing_source_is_noop(
    tmp_path: Path,
) -> None:
    processed = tmp_path / "processed"

    FileFinalizer(
        processed_dir=processed,
        archive_flag=True,
    ).finalize(tmp_path / "missing.md")

    assert not processed.exists()
