from pathlib import Path

from src.ingestion.cleaners.text import TextDocumentCleaner
from src.ingestion.context import DocumentInput, ParsedDocument


def test_text_cleaner():
    document = DocumentInput(
        source="filesystem",
        source_uri="data/raw/billing/policy.md",
        path=Path("data/raw/billing/policy.md"),
    )

    parsed = ParsedDocument(
        document=document,
        content=("\r\n# Billing Policy   \r\n\r\n\r\n\r\nCustomers are billed monthly.   \r\n"),
        content_hash="a" * 64,
        format="markdown",
    )

    cleaner = TextDocumentCleaner()

    result = cleaner.clean(parsed)

    assert result.content == ("# Billing Policy\n\nCustomers are billed monthly.")

    assert result.content_hash == parsed.content_hash
    assert result.format == "markdown"
