from uuid import uuid4

import pytest

from src.models.retrieval import RetrievalResult
from src.models.retrieval_evaluation import (
    EvaluationChunkReference,
    RetrievalEvaluationCase,
)
from src.services.retrieval_evaluation_runner import (
    RetrievalEvaluationRunner,
)
from src.services.retrieval_metrics_service import (
    RetrievalMetricsService,
)

DOC = "data/raw/billing/sample-policy.md"


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


class FakeEvaluationResolver:
    def __init__(self, resolved_by_reference):
        self.resolved_by_reference = resolved_by_reference
        self.references = []

    def resolve_all(self, references):
        self.references.append(references)

        return [
            self.resolved_by_reference[(reference.document, reference.chunk_index)]
            for reference in references
        ]


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


def make_runner(
    results_by_query,
    resolved_by_reference,
):
    pipeline = FakeRetrievalPipeline(results_by_query)
    resolver = FakeEvaluationResolver(resolved_by_reference)

    runner = RetrievalEvaluationRunner(
        retrieval_pipeline=pipeline,
        metrics_service=RetrievalMetricsService(),
        evaluation_resolver=resolver,
    )

    return runner, pipeline, resolver


def test_runner_executes_retrieval_cases():
    relevant_chunk = uuid4()
    irrelevant_chunk = uuid4()

    runner, pipeline, _ = make_runner(
        {
            "What is billing?": [
                make_result(relevant_chunk),
                make_result(irrelevant_chunk),
            ],
        },
        {(DOC, 0): relevant_chunk},
    )

    cases = [
        RetrievalEvaluationCase(
            case_id="billing-001",
            query="What is billing?",
            relevant_chunks=[
                EvaluationChunkReference(
                    document=DOC,
                    chunk_index=0,
                )
            ],
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

    runner, _, _ = make_runner(
        {
            "query-a": [make_result(chunk_a)],
            "query-b": [
                make_result(uuid4()),
                make_result(chunk_b),
            ],
        },
        {
            (DOC, 0): chunk_a,
            (DOC, 1): chunk_b,
        },
    )

    cases = [
        RetrievalEvaluationCase(
            case_id="case-a",
            query="query-a",
            relevant_chunks=[
                EvaluationChunkReference(
                    document=DOC,
                    chunk_index=0,
                )
            ],
        ),
        RetrievalEvaluationCase(
            case_id="case-b",
            query="query-b",
            relevant_chunks=[
                EvaluationChunkReference(
                    document=DOC,
                    chunk_index=1,
                )
            ],
        ),
    ]

    metrics = runner.evaluate(
        cases=cases,
        k=2,
    )

    assert metrics.recall_at_k == 1.0
    assert metrics.precision_at_k == 0.75
    assert metrics.mrr == 0.75


def test_runner_resolves_stable_references():
    relevant_chunk = uuid4()
    irrelevant_chunk = uuid4()

    runner, _, resolver = make_runner(
        {
            "What is billing?": [
                make_result(relevant_chunk),
                make_result(irrelevant_chunk),
            ],
        },
        {(DOC, 0): relevant_chunk},
    )

    reference = EvaluationChunkReference(
        document=DOC,
        chunk_index=0,
    )

    cases = [
        RetrievalEvaluationCase(
            case_id="billing-001",
            query="What is billing?",
            relevant_chunks=[reference],
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

    assert resolver.references == [[reference]]


def test_runner_uses_retrieval_results_and_resolved_references():
    retrieved_chunk = uuid4()
    relevant_chunk = uuid4()

    runner, _, _ = make_runner(
        {"query": [make_result(retrieved_chunk)]},
        {("data/raw/example.md", 0): relevant_chunk},
    )

    cases = [
        RetrievalEvaluationCase(
            case_id="case-1",
            query="query",
            relevant_chunks=[
                EvaluationChunkReference(
                    document="data/raw/example.md",
                    chunk_index=0,
                )
            ],
        )
    ]

    metrics = runner.evaluate(
        cases=cases,
        k=1,
    )

    assert metrics.recall_at_k == 0.0
    assert metrics.precision_at_k == 0.0
    assert metrics.mrr == 0.0
    assert metrics.ndcg_at_k == 0.0


def test_runner_rejects_invalid_k_without_calling_retrieval():
    runner, pipeline, _ = make_runner({}, {})

    with pytest.raises(
        ValueError,
        match="k must be greater than 0",
    ):
        runner.evaluate(cases=[], k=0)

    assert pipeline.requests == []


def test_runner_empty_cases_returns_zero_metrics():
    runner, pipeline, _ = make_runner({}, {})

    metrics = runner.evaluate(cases=[], k=5)

    assert metrics.recall_at_k == 0.0
    assert metrics.precision_at_k == 0.0
    assert metrics.mrr == 0.0
    assert metrics.ndcg_at_k == 0.0

    assert pipeline.requests == []
