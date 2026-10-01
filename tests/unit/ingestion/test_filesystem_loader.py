from pathlib import Path

from src.core.hashing import calculate_file_hash
from src.ingestion.context import DocumentInput
from src.ingestion.loaders.filesystem import FilesystemLoader


def test_filesystem_loader(tmp_path: Path):
    document_path = tmp_path / "policy.md"

    content = "# Billing Policy\n\nCustomers are billed monthly."

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

    loader = FilesystemLoader()

    result = loader.load(
        document=document,
        content_hash=content_hash,
    )

    assert result.document == document
    assert result.content == content
    assert result.content_hash == content_hash
