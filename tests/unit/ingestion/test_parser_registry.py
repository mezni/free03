import pytest

from src.ingestion.parsers.markdown import MarkdownParser
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.parsers.text import TextParser


def test_registry_selects_markdown_parser():
    registry = ParserRegistry(
        parsers=[
            MarkdownParser(),
            TextParser(),
        ]
    )

    parser = registry.get_parser("data/raw/billing/policy.md")

    assert isinstance(parser, MarkdownParser)


def test_registry_selects_text_parser():
    registry = ParserRegistry(
        parsers=[
            MarkdownParser(),
            TextParser(),
        ]
    )

    parser = registry.get_parser("data/raw/billing/policy.txt")

    assert isinstance(parser, TextParser)


def test_registry_rejects_unsupported_format():
    registry = ParserRegistry(
        parsers=[
            MarkdownParser(),
            TextParser(),
        ]
    )

    with pytest.raises(ValueError, match="No parser available"):
        registry.get_parser("data/raw/billing/policy.docx")
