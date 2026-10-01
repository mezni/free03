from uuid import UUID

from sqlalchemy.orm import Session

from src.core.enums import (
    DocumentProcessingOperation,
    DocumentProcessingStatus,
)
from src.db.repositories.document_processing import (
    DocumentProcessingRepository,
)


class DocumentProcessingService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = DocumentProcessingRepository(session)

    def record_success(
        self,
        *,
        run_id: UUID,
        source_uri: str,
        operation: DocumentProcessingOperation,
        document_id: UUID | None = None,
    ):
        record = self.repository.create(
            run_id=run_id,
            source_uri=source_uri,
            operation=operation.value,
            status=DocumentProcessingStatus.SUCCESS.value,
            document_id=document_id,
        )

        self.session.commit()

        return record

    def record_skipped(
        self,
        *,
        run_id: UUID,
        source_uri: str,
        document_id: UUID | None = None,
    ):
        record = self.repository.create(
            run_id=run_id,
            source_uri=source_uri,
            operation=DocumentProcessingOperation.SKIP.value,
            status=DocumentProcessingStatus.SKIPPED.value,
            document_id=document_id,
        )

        self.session.commit()

        return record

    def record_failure(
        self,
        *,
        run_id: UUID,
        source_uri: str,
        operation: DocumentProcessingOperation,
        error_message: str,
        document_id: UUID | None = None,
    ):
        record = self.repository.create(
            run_id=run_id,
            source_uri=source_uri,
            operation=operation.value,
            status=DocumentProcessingStatus.FAILED.value,
            document_id=document_id,
            error_message=error_message,
        )

        self.session.commit()

        return record
