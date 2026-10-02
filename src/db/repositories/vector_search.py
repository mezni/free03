from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from src.db.models.chunk import ChunkDB
from src.db.models.document import DocumentDB
from src.db.models.embedding import EmbeddingDB
from src.models.retrieval import RetrievalFilter


class VectorSearchRepository:
    """Vector similarity search over a single index version."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def search(
        self,
        query_vector: list[float],
        index_version_id: UUID,
        top_k: int,
        filters: RetrievalFilter | None = None,
        knowledge_base_id: UUID | None = None,
    ) -> list[tuple[ChunkDB, float]]:
        distance = EmbeddingDB.vector.cosine_distance(query_vector)

        statement: Select = (
            select(
                ChunkDB,
                distance.label("distance"),
            )
            .join(
                EmbeddingDB,
                EmbeddingDB.chunk_id == ChunkDB.id,
            )
            .join(
                DocumentDB,
                DocumentDB.id == ChunkDB.document_id,
            )
            .where(
                ChunkDB.index_version_id == index_version_id,
            )
            .order_by(distance)
            .limit(top_k)
        )

        if knowledge_base_id is not None:
            statement = statement.where(
                DocumentDB.knowledge_base_id == knowledge_base_id,
            )

        if filters is not None:
            if filters.source is not None:
                statement = statement.where(
                    DocumentDB.source == filters.source,
                )

            if filters.document_id is not None:
                statement = statement.where(
                    DocumentDB.id == filters.document_id,
                )

            if filters.document_type is not None:
                statement = statement.where(
                    DocumentDB.document_type == filters.document_type,
                )

        result = self.session.execute(statement)

        return [(chunk, float(distance_value)) for chunk, distance_value in result.all()]
