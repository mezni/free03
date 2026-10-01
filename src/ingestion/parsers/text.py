from pathlib import Path

from src.ingestion.context import ParsedDocument, RawDocument
from src.ingestion.parsers.base import DocumentParser


class TextParser(DocumentParser):
    """Parser for plain-text documents."""

    SUPPORTED_EXTENSIONS = {".txt"}

    def supports(self, source_uri: str) -> bool:
        extension = Path(source_uri).suffix.lower()

        return extension in self.SUPPORTED_EXTENSIONS

    def parse(self, document: RawDocument) -> ParsedDocument:
        if not self.supports(document.document.source_uri):
            raise ValueError(f"Unsupported document format: {document.document.source_uri}")

        return ParsedDocument(
            document=document.document,
            content=document.content,
            content_hash=document.content_hash,
            format="text",
        )
