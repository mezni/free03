from abc import ABC, abstractmethod

from src.ingestion.context import ParsedDocument, RawDocument


class DocumentParser(ABC):
    """Base interface for document parsers."""

    @abstractmethod
    def supports(self, source_uri: str) -> bool:
        """Return whether this parser supports the document."""
        raise NotImplementedError

    @abstractmethod
    def parse(self, document: RawDocument) -> ParsedDocument:
        """Parse a raw document."""
        raise NotImplementedError
