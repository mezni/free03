import re

from src.ingestion.cleaning import DocumentCleaner
from src.ingestion.context import CleanedDocument, ParsedDocument


class TextDocumentCleaner(DocumentCleaner):
    """Cleaner for textual documents."""

    def clean(
        self,
        document: ParsedDocument,
    ) -> CleanedDocument:
        content = document.content

        content = self._normalize_line_endings(content)
        content = self._remove_trailing_whitespace(content)
        content = self._collapse_excessive_blank_lines(content)
        content = content.strip()

        return CleanedDocument(
            document=document.document,
            content=content,
            content_hash=document.content_hash,
            format=document.format,
        )

    @staticmethod
    def _normalize_line_endings(content: str) -> str:
        return content.replace("\r\n", "\n").replace("\r", "\n")

    @staticmethod
    def _remove_trailing_whitespace(content: str) -> str:
        return "\n".join(line.rstrip() for line in content.split("\n"))

    @staticmethod
    def _collapse_excessive_blank_lines(content: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", content)
