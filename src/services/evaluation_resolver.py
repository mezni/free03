from uuid import UUID

from src.db.repositories.chunks import ChunkRepository
from src.db.repositories.documents import DocumentRepository
from src.db.repositories.index_versions import IndexVersionRepository
from src.models.retrieval_evaluation import (
    EvaluationChunkReference,
)


class EvaluationResolver:
    """Resolve stable evaluation references to indexed chunk IDs."""

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: ChunkRepository,
        index_version_repository: IndexVersionRepository,
    ) -> None:
        self._document_repository = document_repository
        self._chunk_repository = chunk_repository
        self._index_version_repository = index_version_repository

    def resolve(
        self,
        reference: EvaluationChunkReference,
    ) -> UUID:
        active_version = self._index_version_repository.get_active()

        if active_version is None:
            raise RuntimeError("No active index version exists.")

        document = self._document_repository.get_by_source_uri(reference.document)

        if document is None:
            raise LookupError(f"Evaluation document not found: {reference.document}")

        chunks = self._chunk_repository.get_by_document_id_and_version(
            document_id=document.id,
            index_version_id=active_version.id,
        )

        for chunk in chunks:
            if chunk.chunk_index == reference.chunk_index:
                return chunk.id

        raise LookupError(
            "Evaluation chunk not found: "
            f"document={reference.document}, "
            f"chunk_index={reference.chunk_index}, "
            f"index_version={active_version.version_number}"
        )

    def resolve_all(
        self,
        references: list[EvaluationChunkReference],
    ) -> list[UUID]:
        return [self.resolve(reference) for reference in references]
