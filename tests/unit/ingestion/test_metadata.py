from pathlib import Path

from src.ingestion.context import CleanedDocument, DocumentInput
from src.ingestion.metadata_extractor import FilesystemMetadataExtractor


def test_extract_filesystem_metadata(tmp_path: Path) -> None:
    document_path = tmp_path / "sample-policy.md"

    document_path.write_text(
        "# Billing Policy\n\nCustomers are billed according to their active service plan.\n",
        encoding="utf-8",
    )

    document = CleanedDocument(
        document=DocumentInput(
            source="filesystem",
            source_uri=str(document_path),
            path=document_path,
        ),
        content=(
            "# Billing Policy\n\nCustomers are billed according to their active service plan."
        ),
        content_hash="a" * 64,
        format="markdown",
    )

    extractor = FilesystemMetadataExtractor()

    metadata = extractor.extract(document)

    assert metadata.source == "filesystem"
    assert metadata.file_name == "sample-policy.md"
    assert metadata.extension == ".md"
    assert metadata.document_type == "markdown"
    assert metadata.title == "Billing Policy"
    assert metadata.file_size_bytes > 0
    assert metadata.modified_at is not None
