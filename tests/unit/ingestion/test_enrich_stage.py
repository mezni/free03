from pathlib import Path

from src.ingestion.context import CleanedDocument, DocumentInput
from src.ingestion.metadata_extractor import FilesystemMetadataExtractor
from src.ingestion.stages.enrich import EnrichStage


def test_enrich_stage(tmp_path: Path) -> None:
    document_path = tmp_path / "policy.md"

    document_path.write_text(
        "# Billing Policy\n\nBilling information.\n",
        encoding="utf-8",
    )

    cleaned_document = CleanedDocument(
        document=DocumentInput(
            source="filesystem",
            source_uri=str(document_path),
            path=document_path,
        ),
        content="# Billing Policy\n\nBilling information.",
        content_hash="b" * 64,
        format="markdown",
    )

    stage = EnrichStage(FilesystemMetadataExtractor())

    result = stage.execute(cleaned_document)

    assert result.content == cleaned_document.content
    assert result.content_hash == cleaned_document.content_hash
    assert result.metadata.title == "Billing Policy"
    assert result.metadata.file_name == "policy.md"
