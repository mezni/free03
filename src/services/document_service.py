
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

    def delete_document(self, document_id: UUID) -> None:
        """Delete a document by ID."""
        database_document = self.repository.get_by_id(document_id)

        if database_document is None:
            return None

        self.repository.delete(database_document)
        self.session.commit()

    def list_documents(
        self,
        source: str | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Document], int]:
        """List documents with optional filtering and pagination.

        Builds the query, applies source/status filters, calculates total,
        applies offset and limit, and converts database objects to domain models.
        Pagination logic lives in the route, not the repository.
        """
        from src.db.models.document import DocumentDB as DocumentModel

        query = self.session.query(DocumentModel)

        if source:
            query = query.where(DocumentModel.source == source)

        if status:
            query = query.where(DocumentModel.status == status)

        total = query.count()

        documents = query.offset(offset).limit(limit).all()

        domain_docs = [self.to_domain(doc) for doc in documents]

        return domain_docs, total

    def ingest(self, path: str):
        """Trigger document ingestion from a filesystem path.

        This delegates to the IngestionPipeline rather than implementing
        ingestion logic directly, maintaining the separation between the
        technical pipeline and the product use case.
        """

        from src.ingestion.chunkers.text import CharacterTextChunker
        from src.ingestion.cleaners.text import TextDocumentCleaner
        from src.ingestion.loaders.filesystem import FilesystemLoader
        from src.ingestion.metadata import MetadataExtractor
        from src.ingestion.parsers.registry import ParserRegistry
        from src.ingestion.pipeline import IngestionPipeline
        from src.ingestion.sources.filesystem import FilesystemSource
        from src.ingestion.stages.finalizer import FileFinalizer
        from src.providers.embeddings.local import LocalEmbeddingProvider

        source = FilesystemSource(base_path=path)
        loader = FilesystemLoader()
        parser = ParserRegistry()
        cleaner = TextDocumentCleaner()
        metadata_extractor = MetadataExtractor()
        chunker = CharacterTextChunker()
        embedding_provider = LocalEmbeddingProvider()
        finalizer = FileFinalizer()

        pipeline = IngestionPipeline(
            source=source,
            loader=loader,
            parser=parser,
            cleaner=cleaner,
            metadata_extractor=metadata_extractor,
            chunker=chunker,
            embedding_provider=embedding_provider,
            finalizer=finalizer,
            session=self.session,
        )

        return pipeline.run()

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
