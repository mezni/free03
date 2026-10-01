from pathlib import Path

from src.ingestion.context import DocumentInput, RawDocument
from src.ingestion.parsers.markdown import MarkdownParser
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.parsers.text import TextParser
from src.ingestion.stages.parse import ParseStage


def test_parse_stage():
    document = DocumentInput(
        source="filesystem",
        source_uri="data/raw/billing/policy.md",
        path=Path("data/raw/billing/policy.md"),
    )

    raw_document = RawDocument(
        document=document,
        content="# Billing Policy",
        content_hash="b" * 64,
    )

    registry = ParserRegistry(
        parsers=[
            MarkdownParser(),
            TextParser(),
        ]
    )

    stage = ParseStage(registry)

    result = stage.execute(raw_document)

    assert result.format == "markdown"
    assert result.content == "# Billing Policy"
