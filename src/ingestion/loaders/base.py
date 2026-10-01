from abc import ABC, abstractmethod

from src.ingestion.context import DocumentInput, RawDocument


class DocumentLoader(ABC):
    """Base interface for document loaders."""

    @abstractmethod
    def load(
        self,
        document: DocumentInput,
        content_hash: str,
    ) -> RawDocument:
        """Load raw document content."""
        raise NotImplementedError
