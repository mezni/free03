from uuid import uuid4

import pytest

from src.models.retrieval import RetrievalResult
from src.models.retrieval_evaluation import RetrievalEvaluationCase
from src.services.retrieval_evaluation_runner import (
    RetrievalEvaluationRunner,
)
from src.services.retrieval_metrics_service import (
    RetrievalMetricsService,
)


class FakeRetrievalPipeline:
    def __init__(self, results_by_query):
        self.results_by_query = results_by_query
        self.requests = []

    def execute(self, request):
        self.requests.append(request)

        return self.results_by_query.get(
            request.query,
            [],
        )


def make_result(chunk_id):
    return RetrievalResult(
        chunk_id=chunk_id,
        document_id=uuid4(),
        index_version_id=uuid4(),
        content="test content",
        chunk_index=0,
        score=0.5,
        retrieval_method="vector",
    )


def test_runner_executes_retrieval_cases():
    relevant_chunk = uuid4()
    irrelevant_chunk = uuid4()

    pipeline = FakeRetrievalPipeline(
        {
            "What is billing?": [
                make_result(relevant_chunk),
                make_result(irrelevant_chunk),
            ],
        }
    )

    runner = RetrievalEvaluationRunner(
        retrieval_pipeline=pipeline,
        metrics_service=RetrievalMetricsService(),
    )

    cases = [
        RetrievalEvaluationCase(
            case_id="billing-001",
            query="What is billing?",
            relevant_chunk_ids=[relevant_chunk],
        )
    ]

    metrics = runner.evaluate(
        cases=cases,
        k=2,
    )

    assert metrics.recall_at_k == 1.0
    assert metrics.precision_at_k == 0.5
    assert metrics.mrr == 1.0
    assert metrics.ndcg_at_k == 1.0

    assert len(pipeline.requests) == 1
    assert pipeline.requests[0].query == "What is billing?"
    assert pipeline.requests[0].top_k == 2


def test_runner_aggregates_multiple_cases():
    chunk_a = uuid4()
    chunk_b = uuid4()

    pipeline = FakeRetrievalPipeline(
        {
            "query-a": [make_result(chunk_a)],
            "query-b": [
                make_result(uuid4()),
                make_result(chunk_b),
            ],
        }
    )

    runner = RetrievalEvaluationRunner(
        retrieval_pipeline=pipeline,
        metrics_service=RetrievalMetricsService(),
    )

    cases = [
        RetrievalEvaluationCase(
            case_id="case-a",
            query="query-a",
            relevant_chunk_ids=[chunk_a],
        ),
        RetrievalEvaluationCase(
            case_id="case-b",
            query="query-b",
            relevant_chunk_ids=[chunk_b],
        ),
    ]

    metrics = runner.evaluate(
        cases=cases,
        k=2,
    )

    assert metrics.recall_at_k == 1.0
    assert metrics.precision_at_k == 0.75
    assert metrics.mrr == 0.75


def test_runner_rejects_invalid_k_without_calling_retrieval():
    pipeline = FakeRetrievalPipeline({})

    runner = RetrievalEvaluationRunner(
        retrieval_pipeline=pipeline,
        metrics_service=RetrievalMetricsService(),
    )

    with pytest.raises(
        ValueError,
        match="k must be greater than 0",
    ):
        runner.evaluate(cases=[], k=0)

    assert pipeline.requests == []


def test_runner_empty_cases_returns_zero_metrics():
    pipeline = FakeRetrievalPipeline({})

    runner = RetrievalEvaluationRunner(
        retrieval_pipeline=pipeline,
        metrics_service=RetrievalMetricsService(),
    )

    metrics = runner.evaluate(cases=[], k=5)

    assert metrics.recall_at_k == 0.0
    assert metrics.precision_at_k == 0.0
    assert metrics.mrr == 0.0
    assert metrics.ndcg_at_k == 0.0

    assert pipeline.requests == []