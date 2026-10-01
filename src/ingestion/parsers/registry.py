from src.ingestion.parsers.base import DocumentParser


class ParserRegistry:
    """Registry responsible for selecting document parsers."""

    def __init__(self, parsers: list[DocumentParser]) -> None:
        self.parsers = parsers

    def get_parser(self, source_uri: str) -> DocumentParser:
        for parser in self.parsers:
            if parser.supports(source_uri):
                return parser

        raise ValueError(f"No parser available for document: {source_uri}")
