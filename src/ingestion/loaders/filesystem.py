from src.ingestion.context import DocumentInput, RawDocument
from src.ingestion.loaders.base import DocumentLoader


class FilesystemLoader(DocumentLoader):
    """Load text content from a filesystem document."""

    def load(
        self,
        document: DocumentInput,
        content_hash: str,
    ) -> RawDocument:
        content = document.path.read_text(
            encoding="utf-8",
        )

        return RawDocument(
            document=document,
            content=content,
            content_hash=content_hash,
        )
