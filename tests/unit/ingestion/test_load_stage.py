from pathlib import Path

from src.core.enums import DocumentChangeType
from src.core.hashing import calculate_file_hash
from src.ingestion.context import DocumentChange, DocumentInput
from src.ingestion.loaders.filesystem import FilesystemLoader
from src.ingestion.stages.load import LoadStage


def test_load_stage(tmp_path: Path):
    document_path = tmp_path / "policy.md"

    content = "# Billing Policy"

    document_path.write_text(
        content,
        encoding="utf-8",
    )

    document = DocumentInput(
        source="filesystem",
        source_uri=str(document_path),
        path=document_path,
    )

    content_hash = calculate_file_hash(document_path)

    change = DocumentChange(
        document=document,
        change_type=DocumentChangeType.NEW,
        content_hash=content_hash,
    )

    stage = LoadStage(FilesystemLoader())

    result = stage.execute(change)

    assert result.content == content
    assert result.content_hash == content_hash
