from abc import ABC, abstractmethod

from src.ingestion.context import CleanedDocument, DocumentMetadata


class MetadataExtractor(ABC):
    """Interface for extracting document metadata."""

    @abstractmethod
    def extract(self, document: CleanedDocument) -> DocumentMetadata:
        raise NotImplementedError
