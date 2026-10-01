from abc import ABC, abstractmethod

from src.ingestion.context import CleanedDocument, ParsedDocument


class DocumentCleaner(ABC):
    """Base interface for document cleaners."""

    @abstractmethod
    def clean(
        self,
        document: ParsedDocument,
    ) -> CleanedDocument:
        """Clean parsed document content."""
        raise NotImplementedError
