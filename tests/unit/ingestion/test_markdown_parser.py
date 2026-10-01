from pathlib import Path

from src.ingestion.context import DocumentInput, RawDocument
from src.ingestion.parsers.markdown import MarkdownParser


def test_markdown_parser():
    document = DocumentInput(
        source="filesystem",
        source_uri="data/raw/billing/policy.md",
        path=Path("data/raw/billing/policy.md"),
    )

    raw_document = RawDocument(
        document=document,
        content="# Billing Policy\n\nCustomers are billed monthly.",
        content_hash="a" * 64,
    )

    parser = MarkdownParser()

    result = parser.parse(raw_document)

    assert result.format == "markdown"
    assert result.content == raw_document.content
    assert result.content_hash == raw_document.content_hash
