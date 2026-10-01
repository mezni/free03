from uuid import uuid4

from src.models.retrieval import RetrievalFilter, RetrievalQuery
from src.retrieval.search.keyword import KeywordSearchStrategy


class FakeKeywordSearchRepository:
    def __init__(self) -> None:
        self.query = None
        self.top_k = None
        self.filters = None

    def search(
        self,
        query,
        index_version_id,
        top_k,
        filters=None,
    ):
        self.query = query
        self.index_version_id = index_version_id
        self.top_k = top_k
        self.filters = filters

        class FakeChunk:
            id = uuid4()
            document_id = uuid4()
            index_version_id = uuid4()
            content = "Refunds are available within 30 days."
            chunk_index = 0

        return [(FakeChunk(), 0.85)]


def test_keyword_search_strategy():
    repository = FakeKeywordSearchRepository()

    strategy = KeywordSearchStrategy(
        repository=repository,
    )

    filters = RetrievalFilter(
        document_type="policy",
    )

    request = RetrievalQuery(
        query="refund policy",
        top_k=5,
        filters=filters,
    )

    index_version_id = uuid4()

    results = strategy.search(request, index_version_id)

    assert len(results) == 1
    assert results[0].content == "Refunds are available within 30 days."
    assert results[0].score == 0.85
    assert results[0].retrieval_method == "keyword"

    assert repository.index_version_id == index_version_id
    assert repository.query == "refund policy"
    assert repository.top_k == 5
    assert repository.filters == filters
