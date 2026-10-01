from datetime import UTC, datetime

from src.ingestion.context import CleanedDocument, DocumentMetadata
from src.ingestion.metadata import MetadataExtractor


class FilesystemMetadataExtractor(MetadataExtractor):
    """Extract metadata from filesystem documents."""

    def extract(self, document: CleanedDocument) -> DocumentMetadata:
        path = document.document.path
        stat = path.stat()

        return DocumentMetadata(
            source=document.document.source,
            source_uri=document.document.source_uri,
            file_name=path.name,
            extension=path.suffix.lower(),
            document_type=document.format,
            title=self._extract_title(document.content, document.format),
            file_size_bytes=stat.st_size,
            modified_at=datetime.fromtimestamp(
                stat.st_mtime,
                tz=UTC,
            ),
        )

    @staticmethod
    def _extract_title(content: str, document_format: str) -> str | None:
        if document_format == "markdown":
            for line in content.splitlines():
                line = line.strip()

                if line.startswith("# "):
                    title = line[2:].strip()
                    return title or None

        return None
