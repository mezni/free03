from abc import ABC, abstractmethod

from src.ingestion.context import DocumentInput


class DocumentSource(ABC):
    """Base interface for document sources."""

    @abstractmethod
    def discover(self) -> list[DocumentInput]:
        """Discover documents from the source."""
        raise NotImplementedError
