from src.core.enums import DocumentChangeType
from src.core.hashing import calculate_file_hash
from src.ingestion.context import DocumentChange, DocumentInput


class ChangeDetector:
    """Detect whether a document is new, modified, or unchanged."""

    def detect(
        self,
        document: DocumentInput,
        previous_content_hash: str | None,
    ) -> DocumentChange:
        current_hash = calculate_file_hash(document.path)

        if previous_content_hash is None:
            change_type = DocumentChangeType.NEW

        elif current_hash != previous_content_hash:
            change_type = DocumentChangeType.MODIFIED

        else:
            change_type = DocumentChangeType.UNCHANGED

        return DocumentChange(
            document=document,
            change_type=change_type,
            content_hash=current_hash,
            previous_content_hash=previous_content_hash,
        )
