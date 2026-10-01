from uuid import uuid4

from src.models.retrieval import RetrievalFilter, RetrievalQuery
from src.retrieval.search.vector import VectorSearchStrategy


class FakeEmbeddingProvider:
    def __init__(self) -> None:
        self.dimensions = 8

    def embed_query(self, query: str) -> list[float]:
        return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]


class FakeVectorSearchRepository:
    def __init__(self) -> None:
        self.received_query_vector = None
        self.received_top_k = None
        self.received_filters = None
        self.dimensions = 8

    def search(
        self,
        query_vector,
        top_k,
        filters=None,
    ):
        self.received_query_vector = query_vector
        self.received_top_k = top_k
        self.received_filters = filters

        chunk_id = uuid4()
        document_id = uuid4()
        index_version_id = uuid4()

        class FakeChunk:
            def __init__(self):
                self.id = chunk_id
                self.document_id = document_id
                self.index_version_id = index_version_id
                self.content = "Refunds are available within 30 days."
                self.chunk_index = 0

        # Return iterable of (chunk, distance) tuples
        return [(FakeChunk(), 0.15)]


def test_vector_search_strategy_maps_repository_result():
    repository = FakeVectorSearchRepository()

    strategy = VectorSearchStrategy(
        repository=repository,
        embedding_provider=FakeEmbeddingProvider(),
    )

    filters = RetrievalFilter(
        source="filesystem",
        document_type="policy",
    )

    request = RetrievalQuery(
        query="What is the refund policy?",
        top_k=5,
        filters=filters,
    )

    results = strategy.search(request)

    assert len(results) == 1

    result = results[0]

    assert result.content == "Refunds are available within 30 days."
    assert result.chunk_index == 0
    assert result.score == 0.15
    assert result.retrieval_method == "vector"

    assert repository.received_query_vector == [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    assert repository.received_top_k == 5
    assert repository.received_filters == filters
