from uuid import UUID

from sqlalchemy.orm import Session

from src.core.enums import DocumentLifecycleStatus
from src.db.repositories.documents import DocumentRepository
from src.models.document import Document, DocumentCreate


class DocumentService:
    """Application service for document operations."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = DocumentRepository(session)

    def create_document(self, data: DocumentCreate) -> Document:
        """Create and persist a document."""
        database_document = self.repository.create(data)

        self.session.commit()

        return self.repository.to_domain(database_document)

    def get_document(self, document_id: UUID) -> Document | None:
        """Retrieve a document by ID."""
        return self.repository.get_domain_by_id(document_id)

    def get_by_source_uri(self, source_uri: str) -> Document | None:
        """Retrieve a document by source URI."""
        database_document = self.repository.get_by_source_uri(source_uri)

        if database_document is None:
            return None

        return self.repository.to_domain(database_document)

    def delete_document(self, document_id: UUID) -> bool:
        """Delete a document by ID."""
        database_document = self.repository.get_by_id(document_id)

        if database_document is None:
            return False

        self.repository.delete(database_document)
        self.session.commit()

        return True

    def set_processing(self, document_id: UUID) -> Document | None:
        document = self.repository.get_by_id(document_id)

        if document is None:
            return None

        self.repository.update_status(
            document,
            DocumentLifecycleStatus.PROCESSING,
        )
        self.session.commit()

        return self.repository.to_domain(document)

    def set_active(self, document_id: UUID) -> Document | None:
        document = self.repository.get_by_id(document_id)

        if document is None:
            return None

        self.repository.update_status(
            document,
            DocumentLifecycleStatus.ACTIVE,
        )
        self.session.commit()

        return self.repository.to_domain(document)

    def set_failed(self, document_id: UUID) -> Document | None:
        document = self.repository.get_by_id(document_id)

        if document is None:
            return None

        self.repository.update_status(
            document,
            DocumentLifecycleStatus.FAILED,
        )
        self.session.commit()

        return self.repository.to_domain(document)
