from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models.document_processing import DocumentProcessingDB


class DocumentProcessingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        *,
        run_id: UUID,
        source_uri: str,
        operation: str,
        status: str,
        document_id: UUID | None = None,
        error_message: str | None = None,
    ) -> DocumentProcessingDB:
        record = DocumentProcessingDB(
            run_id=run_id,
            document_id=document_id,
            source_uri=source_uri,
            operation=operation,
            status=status,
            error_message=error_message,
        )

        self.session.add(record)
        self.session.flush()

        return record

    def get_by_run_id(
        self,
        run_id: UUID,
    ) -> list[DocumentProcessingDB]:
        statement = (
            select(DocumentProcessingDB)
            .where(DocumentProcessingDB.run_id == run_id)
            .order_by(DocumentProcessingDB.created_at)
        )

        return list(self.session.execute(statement).scalars().all())
