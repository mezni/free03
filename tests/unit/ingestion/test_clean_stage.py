from pathlib import Path

from src.ingestion.cleaners.text import TextDocumentCleaner
from src.ingestion.context import DocumentInput, ParsedDocument
from src.ingestion.stages.clean import CleanStage


def test_clean_stage():
    document = DocumentInput(
        source="filesystem",
        source_uri="data/raw/billing/policy.md",
        path=Path("data/raw/billing/policy.md"),
    )

    parsed = ParsedDocument(
        document=document,
        content="  # Billing Policy  \n\n\n\n",
        content_hash="b" * 64,
        format="markdown",
    )

    stage = CleanStage(TextDocumentCleaner())

    result = stage.execute(parsed)

    assert result.content == "# Billing Policy"
