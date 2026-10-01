from uuid import uuid4

import pytest

from src.evaluation.metrics.retrieval import (
    ContextPrecision,
    ContextRecall,
    MeanReciprocalRank,
    NDCGAtK,
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


def test_ndcg_at_k_ideal_ranking():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a, chunk_b],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = NDCGAtK()

    assert metric.calculate(evaluation, k=2) == pytest.approx(1.0)


def test_ndcg_at_k_partial_relevance():
    chunk_a = uuid4()
    chunk_b = uuid4()

    evaluation = make_evaluation(
        retrieved_ids=[chunk_a, uuid4(), chunk_b],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = NDCGAtK()

    result = metric.calculate(evaluation, k=3)

    assert 0.0 < result < 1.0


def test_ndcg_at_k_no_relevant_results():
    evaluation = make_evaluation(
        retrieved_ids=[uuid4(), uuid4()],
        relevant_ids=[uuid4()],
    )

    metric = NDCGAtK()

    assert metric.calculate(evaluation, k=2) == 0.0


def test_ndcg_at_k_rewards_relevant_results_near_top():
    chunk_a = uuid4()
    chunk_b = uuid4()

    early = make_evaluation(
        retrieved_ids=[chunk_a, chunk_b, uuid4()],
        relevant_ids=[chunk_a, chunk_b],
    )

    late = make_evaluation(
        retrieved_ids=[uuid4(), chunk_a, chunk_b],
        relevant_ids=[chunk_a, chunk_b],
    )

    metric = NDCGAtK()

    early_score = metric.calculate(early, k=3)
    late_score = metric.calculate(late, k=3)

    assert early_score > late_score


def test_ndcg_at_k_rejects_invalid_k():
    evaluation = make_evaluation(
        retrieved_ids=[],
        relevant_ids=[uuid4()],
    )

    metric = NDCGAtK()

    with pytest.raises(ValueError, match="k must be greater than 0"):
        metric.calculate(evaluation, k=0)

class TestContextRecall:
    def test_all_relevant_chunks_in_context(self):
        chunk_a = uuid4()
        chunk_b = uuid4()

        evaluation = make_evaluation(
            retrieved_ids=[chunk_a, chunk_b],
            relevant_ids=[chunk_a, chunk_b],
        )

        metric = ContextRecall()

        assert metric.calculate(
            evaluation,
            [str(chunk_a), str(chunk_b)],
        ) == 1.0

    def test_half_of_relevant_chunks_in_context(self):
        chunk_a = uuid4()
        chunk_b = uuid4()

        evaluation = make_evaluation(
            retrieved_ids=[chunk_a],
            relevant_ids=[chunk_a, chunk_b],
        )

        metric = ContextRecall()

        assert metric.calculate(
            evaluation,
            [str(chunk_a)],
        ) == 0.5

    def test_context_recall_zero_when_context_empty(self):
        evaluation = make_evaluation(
            retrieved_ids=[],
            relevant_ids=[uuid4()],
        )

        metric = ContextRecall()

        assert metric.calculate(evaluation, []) == 0.0

    def test_context_recall_zero_without_relevant_chunks(self):
        evaluation = make_evaluation(
            retrieved_ids=[],
            relevant_ids=[],
        )

        metric = ContextRecall()

        assert metric.calculate(evaluation, []) == 0.0

    def test_perfect_ranking_can_still_fail_context_recall(self):
        """A chunk ranked first but dropped before the LLM.

        Window expansion can push a highly-ranked chunk out of the
        final budget. Context Recall is what catches that.
        """
        relevant = uuid4()

        evaluation = make_evaluation(
            retrieved_ids=[relevant],
            relevant_ids=[relevant],
        )

        assert RecallAtK().calculate(evaluation, k=5) == 1.0
        assert (
            ContextRecall().calculate(evaluation, [])
            == 0.0
        )


class TestContextPrecision:
    def test_all_context_chunks_relevant(self):
        chunk_a = uuid4()
        chunk_b = uuid4()

        evaluation = make_evaluation(
            retrieved_ids=[chunk_a, chunk_b],
            relevant_ids=[chunk_a, chunk_b],
        )

        metric = ContextPrecision()

        assert metric.calculate(
            evaluation,
            [str(chunk_a), str(chunk_b)],
        ) == 1.0

    def test_neighbor_padding_lowers_precision(self):
        """Window expansion adds chunks nobody judged relevant."""
        relevant = uuid4()

        evaluation = make_evaluation(
            retrieved_ids=[relevant],
            relevant_ids=[relevant],
        )

        metric = ContextPrecision()

        assert metric.calculate(
            evaluation,
            [
                str(relevant),
                str(uuid4()),
                str(uuid4()),
            ],
        ) == pytest.approx(1 / 3)

    def test_context_precision_zero_when_empty(self):
        evaluation = make_evaluation(
            retrieved_ids=[],
            relevant_ids=[],
        )

        metric = ContextPrecision()

        assert metric.calculate(evaluation, []) == 0.0
