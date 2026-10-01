from abc import ABC, abstractmethod

from src.ingestion.context import DocumentChunk, EnrichedDocument


class DocumentChunker(ABC):
    """Interface for splitting documents into chunks."""

    @abstractmethod
    def chunk(self, document: EnrichedDocument) -> list[DocumentChunk]:
        raise NotImplementedError
