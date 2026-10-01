from uuid import UUID

from src.db.repositories.keyword_search import KeywordSearchRepository
from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.retrieval.search.base import SearchStrategy


class KeywordSearchStrategy(SearchStrategy):
    """
    PostgreSQL full-text search strategy.
    """

    def __init__(
        self,
        repository: KeywordSearchRepository,
    ) -> None:
        self.repository = repository

    def search(
        self,
        request: RetrievalQuery,
        index_version_id: UUID,
    ) -> list[RetrievalResult]:
        rows = self.repository.search(
            query=request.query,
            index_version_id=index_version_id,
            top_k=request.top_k,
            filters=request.filters,
        )

        return [
            RetrievalResult(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                index_version_id=chunk.index_version_id,
                content=chunk.content,
                chunk_index=chunk.chunk_index,
                score=rank,
                retrieval_method="keyword",
            )
            for chunk, rank in rows
        ]
