from uuid import uuid4

from src.models.retrieval import RetrievalFilter, RetrievalQuery, RetrievalResult
from src.retrieval.pipeline import RetrievalPipeline


class FakeRetrievalService:
    def __init__(self, results: list[RetrievalResult]) -> None:
        self.results = results
        self.received_request: RetrievalQuery | None = None

    def search(
        self,
        request: RetrievalQuery,
    ) -> list[RetrievalResult]:
        self.received_request = request
        return self.results


class FakeReranker:
    def __init__(self) -> None:
        self.query = None
        self.candidates = None
        self.top_k = None

    def rerank(self, query, candidates, top_k):
        self.query = query
        self.candidates = candidates
        self.top_k = top_k

        return [
            candidate.model_copy(update={"retrieval_method": "reranked"})
            for candidate in candidates[:top_k]
        ]


class StubQueryAnalyzer:
    def __init__(
        self,
        rewritten: str,
        filters=None,
    ) -> None:
        self.rewritten = rewritten
        self.filters = filters
        self.queries: list[str] = []

    def analyze(self, query):
        from src.models.query_analysis import QueryAnalysis

        self.queries.append(query)

        return QueryAnalysis(
            original_query=query,
            rewritten_query=self.rewritten,
            filters=self.filters,
        )


class StubContextWindowService:
    def __init__(self, expanded) -> None:
        self.expanded = expanded
        self.calls: list[tuple] = []

    def expand(self, results, window=1):
        self.calls.append((results, window))
        return self.expanded


class StubContextSelector:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def select(self, results, max_chunks):
        self.calls.append((results, max_chunks))
        return results[:max_chunks]


def make_result(
    content: str = "result",
    chunk_index: int = 0,
) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        index_version_id=uuid4(),
        content=content,
        chunk_index=chunk_index,
        score=0.1,
        retrieval_method="vector",
    )


def test_pipeline_delegates_to_retrieval_service():
    expected_results = [make_result("Refunds are available within 30 days.")]

    service = FakeRetrievalService(expected_results)
    pipeline = RetrievalPipeline(service)

    request = RetrievalQuery(
        query="What is the refund policy?",
        top_k=5,
    )

    results = pipeline.execute(request)

    assert results == expected_results
    assert service.received_request == request


def test_pipeline_reranks_results():
    results = [
        make_result("result 1", 0),
        make_result("result 2", 1),
    ]

    service = FakeRetrievalService(results)
    reranker = FakeReranker()

    pipeline = RetrievalPipeline(
        retrieval_service=service,
        reranker=reranker,
    )

    request = RetrievalQuery(
        query="refund policy",
        top_k=1,
    )

    final_results = pipeline.execute(request)

    assert len(final_results) == 1
    assert final_results[0].content == "result 1"
    assert final_results[0].retrieval_method == "reranked"

    assert reranker.query == "refund policy"
    assert len(reranker.candidates) == 2
    assert reranker.top_k == 1


def test_pipeline_searches_with_rewritten_query():
    service = FakeRetrievalService([make_result()])
    analyzer = StubQueryAnalyzer(rewritten="refund policy rules")

    pipeline = RetrievalPipeline(
        retrieval_service=service,
        query_analyzer=analyzer,
    )

    pipeline.execute(RetrievalQuery(query="  What is   refund?  ", top_k=5))

    assert analyzer.queries == ["  What is   refund?  "]
    assert service.received_request.query == "refund policy rules"


def test_pipeline_passes_analyzer_filters_to_retrieval():
    service = FakeRetrievalService([make_result()])

    filters = RetrievalFilter(document_type="markdown")

    pipeline = RetrievalPipeline(
        retrieval_service=service,
        query_analyzer=StubQueryAnalyzer(
            rewritten="policy",
            filters=filters,
        ),
    )

    pipeline.execute(RetrievalQuery(query="policy", top_k=5))

    assert service.received_request.filters == filters


def test_analyzer_without_filters_keeps_caller_filters():
    service = FakeRetrievalService([make_result()])

    caller_filters = RetrievalFilter(source="filesystem")

    pipeline = RetrievalPipeline(
        retrieval_service=service,
        query_analyzer=StubQueryAnalyzer(
            rewritten="policy",
            filters=None,
        ),
    )

    pipeline.execute(
        RetrievalQuery(
            query="policy",
            top_k=5,
            filters=caller_filters,
        )
    )

    assert service.received_request.filters == caller_filters


def test_no_analyzer_passes_query_through():
    service = FakeRetrievalService([make_result()])

    pipeline = RetrievalPipeline(retrieval_service=service)

    pipeline.execute(RetrievalQuery(query="  raw   query  ", top_k=5))

    assert service.received_request.query == "  raw   query  "


def test_pipeline_expands_context_window():
    original = [make_result("retrieved")]
    expanded = [
        make_result("previous"),
        make_result("retrieved"),
        make_result("next"),
    ]

    window_service = StubContextWindowService(expanded)

    pipeline = RetrievalPipeline(
        retrieval_service=FakeRetrievalService(original),
        context_window_service=window_service,
    )

    results = pipeline.execute(RetrievalQuery(query="q", top_k=5))

    assert results == expanded
    assert window_service.calls[0][1] == 1


def test_pipeline_selects_context_after_expansion():
    original = [make_result("a"), make_result("b")]
    expanded = [
        make_result("a"),
        make_result("a-neighbor"),
        make_result("b"),
        make_result("b-neighbor"),
    ]

    selector = StubContextSelector()

    pipeline = RetrievalPipeline(
        retrieval_service=FakeRetrievalService(original),
        context_window_service=StubContextWindowService(expanded),
        context_selector=selector,
    )

    results = pipeline.execute(RetrievalQuery(query="q", top_k=2))

    assert len(results) == 2
    assert selector.calls[0][1] == 2


def test_context_cap_applies_without_expansion():
    selector = StubContextSelector()

    pipeline = RetrievalPipeline(
        retrieval_service=FakeRetrievalService(
            [make_result("a"), make_result("b"), make_result("c")]
        ),
        context_selector=selector,
    )

    results = pipeline.execute(RetrievalQuery(query="q", top_k=2))

    assert len(results) == 2


def test_candidate_k_widens_retrieval_pool():
    """Reranking can only reorder what retrieval returned."""
    service = FakeRetrievalService([make_result()])
    reranker = FakeReranker()

    pipeline = RetrievalPipeline(
        retrieval_service=service,
        reranker=reranker,
        rerank_candidate_k=20,
    )

    pipeline.execute(RetrievalQuery(query="q", top_k=5))

    assert service.received_request.top_k == 20
    assert reranker.top_k == 5


def test_candidate_k_never_narrows_below_caller_top_k():
    service = FakeRetrievalService([make_result()])

    pipeline = RetrievalPipeline(
        retrieval_service=service,
        rerank_candidate_k=3,
    )

    pipeline.execute(RetrievalQuery(query="q", top_k=10))

    assert service.received_request.top_k == 10


def test_max_chunks_sets_context_budget():
    selector = StubContextSelector()

    pipeline = RetrievalPipeline(
        retrieval_service=FakeRetrievalService([make_result()]),
        context_selector=selector,
        max_chunks=8,
    )

    pipeline.execute(RetrievalQuery(query="q", top_k=3))

    assert selector.calls[0][1] == 8


def test_max_chunks_never_truncates_below_caller_top_k():
    """A context cap below top_k would drop results the caller asked
    for. The caller's top_k wins."""
    pipeline = RetrievalPipeline(
        retrieval_service=FakeRetrievalService([make_result()]),
        context_selector=StubContextSelector(),
        max_chunks=2,
    )

    results = pipeline.execute(RetrievalQuery(query="q", top_k=5))

    assert len(results) == 1


def test_window_size_is_passed_through():
    window_service = StubContextWindowService([make_result()])

    pipeline = RetrievalPipeline(
        retrieval_service=FakeRetrievalService([make_result()]),
        context_window_service=window_service,
        window_size=2,
    )

    pipeline.execute(RetrievalQuery(query="q", top_k=5))

    assert window_service.calls[0][1] == 2


def test_no_optional_stages_returns_retrieval_results():
    results = [make_result("a")]

    pipeline = RetrievalPipeline(retrieval_service=FakeRetrievalService(results))

    assert pipeline.execute(RetrievalQuery(query="q", top_k=5)) == results
