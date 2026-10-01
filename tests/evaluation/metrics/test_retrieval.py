from uuid import uuid4

import pytest

from src.evaluation.metrics.retrieval import (
    MeanReciprocalRank,
    PrecisionAtK,
    RecallAtK,
    ReciprocalRank,
)
from src.models.retrieval_evaluation import RetrievalEvaluationResult


def make_evaluation(
    retrieved_ids,
    relevant_ids,
):
    return RetrievalEvaluationResult(
        case_id="case-1",
        retrieved_chunk_ids=retrieved_ids,
        relevant_chunk_ids=relevant_ids,
    )


def test_recall_at_k_all_relevant_chunks_found():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a, chunk_b],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = RecallAtK()

    assert metric.calculate(evaluation, k=2) == 1.0


def test_recall_at_k_half_found():
    chunk_a = uuid4()
    chunk_b = uuid4()
    chunk_c = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a, chunk_c],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = RecallAtK()

    assert metric.calculate(evaluation, k=2) == 0.5


def test_recall_at_k_none_found():
    chunk_a = uuid4()
    chunk_b = uuid4()
    chunk_c = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_c],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = RecallAtK()

    assert metric.calculate(evaluation, k=1) == 0.0


def test_recall_at_k_uses_only_top_k():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[uuid4(), uuid4(), chunk_a, chunk_b],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = RecallAtK()

    assert metric.calculate(evaluation, k=2) == 0.0
    assert metric.calculate(evaluation, k=3) == 0.5
    assert metric.calculate(evaluation, k=4) == 1.0


def test_recall_at_k_larger_than_results():
    chunk_a = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a],
        relevant_ids=[chunk_a],
    )

    metric = RecallAtK()

    assert metric.calculate(evaluation, k=10) == 1.0


def test_recall_at_k_rejects_invalid_k():
    evaluation = make_evaluation(
        retrieved_ids=[],
        relevant_ids=[uuid4()],
    )

    metric = RecallAtK()

    with pytest.raises(ValueError, match="k must be greater than 0"):
        metric.calculate(evaluation, k=0)


def test_precision_at_k_all_results_are_relevant():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a, chunk_b],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = PrecisionAtK()

    assert metric.calculate(evaluation, k=2) == 1.0


def test_precision_at_k_half_results_are_relevant():
    chunk_a = uuid4()
    chunk_b = uuid4()
    chunk_c = uuid4()
    chunk_d = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a, chunk_c, chunk_b, chunk_d],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = PrecisionAtK()

    assert metric.calculate(evaluation, k=4) == 0.5


def test_precision_at_k_none_are_relevant():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a],
        relevant_ids=[chunk_b],
    )

    metric = PrecisionAtK()

    assert metric.calculate(evaluation, k=1) == 0.0


def test_precision_at_k_uses_only_top_k():
    relevant_chunk = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[uuid4(), uuid4(), relevant_chunk],
        relevant_ids=[relevant_chunk],
    )

    metric = PrecisionAtK()

    assert metric.calculate(evaluation, k=2) == 0.0
    assert metric.calculate(evaluation, k=3) == 1 / 3


def test_precision_at_k_empty_results():
    evaluation = make_evaluation(
        retrieved_ids=[],
        relevant_ids=[uuid4()],
    )

    metric = PrecisionAtK()

    assert metric.calculate(evaluation, k=5) == 0.0


def test_precision_at_k_rejects_invalid_k():
    evaluation = make_evaluation(
        retrieved_ids=[],
        relevant_ids=[uuid4()],
    )

    metric = PrecisionAtK()

    with pytest.raises(ValueError, match="k must be greater than 0"):
        metric.calculate(evaluation, k=0)

def test_reciprocal_rank_first_result_is_relevant():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a, chunk_b],
        relevant_ids=[chunk_a],
    )

    metric = ReciprocalRank()

    assert metric.calculate(evaluation, k=2) == 1.0


def test_reciprocal_rank_relevant_result_is_second():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_b, chunk_a],
        relevant_ids=[chunk_a],
    )

    metric = ReciprocalRank()

    assert metric.calculate(evaluation, k=2) == 0.5


def test_reciprocal_rank_relevant_result_is_third():
    chunk_a = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[uuid4(), uuid4(), chunk_a],
        relevant_ids=[chunk_a],
    )

    metric = ReciprocalRank()

    assert metric.calculate(evaluation, k=3) == 1 / 3


def test_reciprocal_rank_returns_zero_when_no_relevant_result():
    evaluation = make_evaluation(
        retrieved_ids=[uuid4(), uuid4()],
        relevant_ids=[uuid4()],
    )

    metric = ReciprocalRank()

    assert metric.calculate(evaluation, k=2) == 0.0


def test_reciprocal_rank_uses_only_top_k():
    chunk_a = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[uuid4(), chunk_a],
        relevant_ids=[chunk_a],
    )

    metric = ReciprocalRank()

    assert metric.calculate(evaluation, k=1) == 0.0
    assert metric.calculate(evaluation, k=2) == 0.5


def test_reciprocal_rank_rejects_invalid_k():
    evaluation = make_evaluation(
        retrieved_ids=[],
        relevant_ids=[uuid4()],
    )

    metric = ReciprocalRank()

    with pytest.raises(ValueError, match="k must be greater than 0"):
        metric.calculate(evaluation, k=0)


def test_mean_reciprocal_rank():
    chunk_a = uuid4()
    chunk_b = uuid4()
    chunk_c = uuid4()

    evaluations = [
        make_evaluation(
            retrieved_ids=[chunk_a, uuid4()],
            relevant_ids=[chunk_a],
        ),
        make_evaluation(
            retrieved_ids=[uuid4(), chunk_b],
            relevant_ids=[chunk_b],
        ),
        make_evaluation(
            retrieved_ids=[uuid4(), uuid4(), chunk_c],
            relevant_ids=[chunk_c],
        ),
    ]

    metric = MeanReciprocalRank()

    result = metric.calculate(evaluations, k=3)

    expected = (1.0 + 0.5 + (1 / 3)) / 3

    assert result == pytest.approx(expected)


def test_mean_reciprocal_rank_empty_dataset():
    metric = MeanReciprocalRank()

    assert metric.calculate([], k=5) == 0.0


def test_mean_reciprocal_rank_rejects_invalid_k():
    metric = MeanReciprocalRank()

    with pytest.raises(ValueError, match="k must be greater than 0"):
        metric.calculate([], k=0)