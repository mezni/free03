from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.enums import DocumentLifecycleStatus
from src.db.models.document import DocumentDB
from src.models.document import Document, DocumentCreate


class DocumentRepository:
    """Persistence operations for documents."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: DocumentCreate) -> DocumentDB:
        document = DocumentDB(
            source=data.source,
            source_uri=data.source_uri,
            title=data.title,
            document_type=data.document_type,
            content_hash=data.content_hash,
            status=data.status,
        )

        self.session.add(document)
        self.session.flush()

        return document

    def get_by_id(self, document_id: UUID) -> DocumentDB | None:
        statement = select(DocumentDB).where(DocumentDB.id == document_id)

        return self.session.execute(statement).scalar_one_or_none()

    def get_by_source_uri(self, source_uri: str) -> DocumentDB | None:
        statement = select(DocumentDB).where(DocumentDB.source_uri == source_uri)

        return self.session.execute(statement).scalar_one_or_none()

    def get_by_content_hash(
        self,
        content_hash: str,
    ) -> DocumentDB | None:
        statement = select(DocumentDB).where(DocumentDB.content_hash == content_hash)

        return self.session.execute(statement).scalar_one_or_none()

    def get_domain_by_id(self, document_id: UUID) -> Document | None:
        document = self.get_by_id(document_id)

        if document is None:
            return None

        return self.to_domain(document)

    @staticmethod
    def to_domain(document: DocumentDB) -> Document:
        return Document(
            id=document.id,
            source=document.source,
            source_uri=document.source_uri,
            title=document.title,
            document_type=document.document_type,
            content_hash=document.content_hash,
            status=DocumentLifecycleStatus(document.status),
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    def delete(self, document: DocumentDB) -> None:
        self.session.delete(document)

    def update_content_hash(
        self,
        document: DocumentDB,
        content_hash: str,
        title: str | None = None,
        document_type: str | None = None,
    ) -> DocumentDB:
        document.content_hash = content_hash
        document.title = title
        document.document_type = document_type

        self.session.flush()

        return document

    def update_status(
        self,
        document: DocumentDB,
        status: DocumentLifecycleStatus,
    ) -> DocumentDB:
        document.status = status.value
        self.session.flush()

        return document
