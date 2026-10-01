from uuid import UUID

from sqlalchemy.orm import Session

from src.core.enums import (
    DocumentLifecycleStatus,
    IndexVersionStatus,
)
from src.db.models.index_version import IndexVersionDB
from src.db.repositories.chunks import ChunkRepository
from src.db.repositories.documents import DocumentRepository
from src.db.repositories.embeddings import EmbeddingRepository
from src.db.repositories.index_versions import IndexVersionRepository
from src.ingestion.context import EmbeddedDocument


class IndexingService:
    """Manage document index lifecycle."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.documents = DocumentRepository(session)
        self.chunks = ChunkRepository(session)
        self.embeddings = EmbeddingRepository(session)
        self.index_versions = IndexVersionRepository(session)

    def add(
        self,
        data: EmbeddedDocument,
        index_version_id: UUID | None = None,
    ) -> UUID:
        """Add a new document to the index (defaults to the active version)."""

        version = self._resolve_version(index_version_id)

        self._validate_writable_version(version)
        self._validate_embedding_dimensions(data, version)

        try:
            document_id = self.add_to_version(
                data=data,
                index_version_id=version.id,
            )

            document = self.documents.get_by_id(document_id)

            if document is not None:
                self.documents.update_status(
                    document,
                    DocumentLifecycleStatus.ACTIVE,
                )

            self.session.commit()

            return document_id

        except Exception:
            self.session.rollback()
            raise

    def update(
        self,
        data: EmbeddedDocument,
        index_version_id: UUID | None = None,
    ) -> UUID:
        """Replace the indexed content for an existing document."""

        version = self._resolve_version(index_version_id)

        self._validate_writable_version(version)
        self._validate_embedding_dimensions(data, version)

        try:
            document = self.documents.get_by_source_uri(data.document.source_uri)

            if document is None:
                raise ValueError("Cannot update document because it does not exist")

            self.documents.update_status(
                document,
                DocumentLifecycleStatus.PROCESSING,
            )

            existing_chunks = self.chunks.get_by_document_id_and_version(
                document.id,
                version.id,
            )

            chunk_ids = [chunk.id for chunk in existing_chunks]

            self.embeddings.delete_by_chunk_ids(chunk_ids)
            self.chunks.delete_by_document_id(
                document.id,
                version.id,
            )

            self.documents.update_content_hash(
                document=document,
                content_hash=data.content_hash,
                title=data.metadata.title,
                document_type=data.metadata.document_type,
            )

            self._persist_chunks_and_embeddings(
                document_id=document.id,
                data=data,
                index_version=version,
            )

            self.documents.update_status(
                document,
                DocumentLifecycleStatus.ACTIVE,
            )

            self.session.commit()

            return document.id

        except Exception:
            self.session.rollback()
            raise

    def delete(
        self,
        document_id: UUID,
        index_version_id: UUID | None = None,
    ) -> None:
        """Remove a document from an index version, keeping the document record."""

        version = self._resolve_version(index_version_id)

        self._validate_writable_version(version)

        self.chunks.delete_by_document_id(
            document_id=document_id,
            index_version_id=version.id,
        )

        self.session.commit()

    def add_to_version(
        self,
        data: EmbeddedDocument,
        index_version_id: UUID,
    ) -> UUID:
        """Persist a document into an explicit BUILDING/ACTIVE version."""

        version = self._resolve_version(index_version_id)

        self._validate_writable_version(version)
        self._validate_embedding_dimensions(data, version)

        try:
            document = self.documents.get_by_source_uri(data.document.source_uri)

            if document is None:
                document = self.documents.create(self._build_document_data(data))

            self._persist_chunks_and_embeddings(
                document_id=document.id,
                data=data,
                index_version=version,
            )

            self.session.flush()

            return document.id

        except Exception:
            self.session.rollback()
            raise

    def _resolve_version(
        self,
        index_version_id: UUID | None,
    ) -> IndexVersionDB:
        if index_version_id is not None:
            version = self.index_versions.get_by_id(index_version_id)

            if version is None:
                raise ValueError(f"Index version not found: {index_version_id}")

            return version

        version = self.index_versions.get_active()

        if version is None:
            raise ValueError("No active index version exists")

        return version

    def _validate_writable_version(
        self,
        version: IndexVersionDB,
    ) -> None:
        if version.status not in {
            IndexVersionStatus.BUILDING.value,
            IndexVersionStatus.ACTIVE.value,
        }:
            raise ValueError(
                f"Index version {version.version_number} is not writable: {version.status}"
            )

    def _validate_embedding_dimensions(
        self,
        data: EmbeddedDocument,
        version: IndexVersionDB,
    ) -> None:
        for embedding in data.embeddings:
            if embedding.dimensions != version.embedding_dimensions:
                raise ValueError(
                    "Embedding dimensions do not match index version: "
                    f"expected {version.embedding_dimensions}, "
                    f"got {embedding.dimensions}"
                )

    def _persist_chunks_and_embeddings(
        self,
        document_id: UUID,
        data: EmbeddedDocument,
        index_version: IndexVersionDB,
    ) -> None:
        for chunk, embedding in zip(
            data.chunks,
            data.embeddings,
            strict=True,
        ):
            database_chunk = self.chunks.create(
                document_id=document_id,
                index_version_id=index_version.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                content_hash=chunk.content_hash,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
            )

            self.embeddings.create(
                chunk_id=database_chunk.id,
                model_name=embedding.model_name,
                dimensions=embedding.dimensions,
                vector=embedding.vector,
            )

    @staticmethod
    def _build_document_data(
        data: EmbeddedDocument,
    ):
        from src.models.document import DocumentCreate

        return DocumentCreate(
            source=data.document.source,
            source_uri=data.document.source_uri,
            title=data.metadata.title,
            document_type=data.metadata.document_type,
            content_hash=data.content_hash,
            status=DocumentLifecycleStatus.PROCESSING,
        )
