from uuid import uuid4

import pytest

from src.models.retrieval_evaluation import RetrievalEvaluationResult
from src.services.retrieval_metrics_service import RetrievalMetricsService


def make_evaluation(
    retrieved_ids,
    relevant_ids,
    case_id,
):
    return RetrievalEvaluationResult(
        case_id=case_id,
        retrieved_chunk_ids=retrieved_ids,
        relevant_chunk_ids=relevant_ids,
    )


def test_evaluate_returns_all_metrics():
    chunk_a = uuid4()
    chunk_b = uuid4()
    irrelevant = uuid4()

    evaluations = [
        make_evaluation(
            retrieved_ids=[chunk_a, irrelevant],
            relevant_ids=[chunk_a, chunk_b],
            case_id="case-1",
        ),
        make_evaluation(
            retrieved_ids=[chunk_b, irrelevant],
            relevant_ids=[chunk_b],
            case_id="case-2",
        ),
    ]

    service = RetrievalMetricsService()

    result = service.evaluate(
        evaluations=evaluations,
        k=2,
    )

    assert result.recall_at_k == pytest.approx(0.75)
    assert result.precision_at_k == pytest.approx(0.5)
    assert result.mrr == pytest.approx(1.0)
    assert result.ndcg_at_k == pytest.approx(0.806574)
    assert 0.0 < result.ndcg_at_k <= 1.0


def test_evaluate_empty_dataset():
    service = RetrievalMetricsService()

    result = service.evaluate(
        evaluations=[],
        k=5,
    )

    assert result.recall_at_k == 0.0
    assert result.precision_at_k == 0.0
    assert result.mrr == 0.0
    assert result.ndcg_at_k == 0.0


def test_evaluate_rejects_invalid_k():
    service = RetrievalMetricsService()

    with pytest.raises(
        ValueError,
        match="k must be greater than 0",
    ):
        service.evaluate(
            evaluations=[],
            k=0,
        )