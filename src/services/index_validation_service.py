from uuid import UUID

from src.core.enums import IndexVersionStatus
from src.db.models.chunk import ChunkDB
from src.db.models.embedding import EmbeddingDB
from src.db.repositories.chunks import ChunkRepository
from src.db.repositories.embeddings import EmbeddingRepository
from src.db.repositories.index_versions import IndexVersionRepository
from src.models.index_validation import IndexValidationResult


class IndexValidationService:
    def __init__(
        self,
        index_version_repository: IndexVersionRepository,
        chunk_repository: ChunkRepository,
        embedding_repository: EmbeddingRepository,
    ) -> None:
        self.index_version_repository = index_version_repository
        self.chunk_repository = chunk_repository
        self.embedding_repository = embedding_repository

    def validate(
        self,
        index_version_id: UUID,
    ) -> IndexValidationResult:
        version = self.index_version_repository.get_by_id(index_version_id)

        if version is None:
            raise ValueError(f"Index version not found: {index_version_id}")

        errors: list[str] = []

        if version.status != IndexVersionStatus.BUILDING.value:
            errors.append(f"Index version must be BUILDING, got {version.status}")

        chunks = self.chunk_repository.get_by_index_version_id(index_version_id)

        embeddings = self.embedding_repository.get_by_index_version_id(index_version_id)

        chunk_count = len(chunks)
        embedding_count = len(embeddings)

        if chunk_count == 0:
            errors.append("Index contains no chunks")

        invalid_embedding_count = sum(
            1 for embedding in embeddings if embedding.dimensions != version.embedding_dimensions
        )

        if invalid_embedding_count > 0:
            errors.append(f"{invalid_embedding_count} embeddings have incorrect dimensions")

        chunks_without_embeddings = self._count_chunks_without_embeddings(
            chunks,
            embeddings,
        )

        if chunks_without_embeddings > 0:
            errors.append(f"{chunks_without_embeddings} chunks have no embedding")

        duplicate_chunk_count = self._count_duplicate_chunks(chunks)

        if duplicate_chunk_count > 0:
            errors.append(f"{duplicate_chunk_count} duplicate chunk positions found")

        return IndexValidationResult(
            valid=not errors,
            document_count=len({chunk.document_id for chunk in chunks}),
            chunk_count=chunk_count,
            embedding_count=embedding_count,
            expected_embedding_dimensions=version.embedding_dimensions,
            invalid_embedding_count=invalid_embedding_count,
            duplicate_chunk_count=duplicate_chunk_count,
            chunks_without_embeddings=chunks_without_embeddings,
            errors=errors,
        )

    def _count_chunks_without_embeddings(
        self,
        chunks: list[ChunkDB],
        embeddings: list[EmbeddingDB],
    ) -> int:
        embedding_chunk_ids = {embedding.chunk_id for embedding in embeddings}

        return sum(1 for chunk in chunks if chunk.id not in embedding_chunk_ids)

    def _count_duplicate_chunks(
        self,
        chunks: list[ChunkDB],
    ) -> int:
        seen: set[tuple[UUID, int]] = set()
        duplicates = 0

        for chunk in chunks:
            key = (
                chunk.document_id,
                chunk.chunk_index,
            )

            if key in seen:
                duplicates += 1
            else:
                seen.add(key)

        return duplicates
