from uuid import UUID

from src.db.repositories.vector_search import VectorSearchRepository
from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.retrieval.search.base import SearchStrategy


class VectorSearchStrategy(SearchStrategy):
    """
    Vector similarity search strategy.

    Delegates persistence-specific searching to the
    VectorSearchRepository and converts persistence
    results into application retrieval results.
    """

    def __init__(
        self,
        repository: VectorSearchRepository,
        embedding_provider,
    ) -> None:
        self.repository = repository
        self.embedding_provider = embedding_provider

    def search(
        self,
        request: RetrievalQuery,
        index_version_id: UUID,
    ) -> list[RetrievalResult]:
        query_vector = self.embedding_provider.embed_query(
            request.query,
        )

        rows = self.repository.search(
            query_vector=query_vector,
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
                score=distance,
                retrieval_method="vector",
            )
            for chunk, distance in rows
        ]
