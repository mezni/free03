from uuid import UUID

from sqlalchemy import func, select

from src.db.models.chunk import ChunkDB
from src.db.models.document import DocumentDB
from src.models.retrieval import RetrievalFilter


class KeywordSearchRepository:
    def __init__(self, session) -> None:
        self.session = session

    def search(
        self,
        query: str,
        index_version_id: UUID,
        top_k: int,
        filters: RetrievalFilter | None = None,
        knowledge_base_id: UUID | None = None,
    ) -> list[tuple[ChunkDB, float]]:
        search_query = func.websearch_to_tsquery(
            "english",
            query,
        )

        rank = func.ts_rank_cd(
            ChunkDB.search_vector,
            search_query,
        )

        statement = (
            select(
                ChunkDB,
                rank.label("rank"),
            )
            .join(
                DocumentDB,
                DocumentDB.id == ChunkDB.document_id,
            )
            .where(
                ChunkDB.search_vector.op("@@")(search_query),
                ChunkDB.index_version_id == index_version_id,
            )
            .order_by(rank.desc())
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

        return [(chunk, float(rank_value)) for chunk, rank_value in result.all()]
