from uuid import uuid4

from src.models.retrieval import RetrievalQuery, RetrievalResult
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
    def __init__(self):
        self.query = None
        self.candidates = None
        self.top_k = None

    def rerank(
        self,
        query,
        candidates,
        top_k,
    ):
        self.query = query
        self.candidates = candidates
        self.top_k = top_k

        return [
            candidate.model_copy(
                update={
                    "retrieval_method": "reranked",
                },
            )
            for candidate in candidates[:top_k]
        ]


def test_pipeline_delegates_to_retrieval_service():
    chunk_id = uuid4()
    document_id = uuid4()
    index_version_id = uuid4()

    expected_results = [
        RetrievalResult(
            chunk_id=chunk_id,
            document_id=document_id,
            index_version_id=index_version_id,
            content="Refunds are available within 30 days.",
            chunk_index=0,
            score=0.1,
            retrieval_method="vector",
        )
    ]

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
        RetrievalResult(
            chunk_id=uuid4(),
            document_id=uuid4(),
            index_version_id=uuid4(),
            content="result 1",
            chunk_index=0,
            score=0.1,
            retrieval_method="vector",
        ),
        RetrievalResult(
            chunk_id=uuid4(),
            document_id=uuid4(),
            index_version_id=uuid4(),
            content="result 2",
            chunk_index=1,
            score=0.2,
            retrieval_method="vector",
        ),
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