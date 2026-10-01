from src.evaluation.metrics.retrieval import (
    MeanReciprocalRank,
    NDCGAtK,
    PrecisionAtK,
    RecallAtK,
)
from src.models.retrieval_evaluation import RetrievalEvaluationResult
from src.models.retrieval_metrics import RetrievalMetrics


class RetrievalMetricsService:
    """Calculate retrieval metrics across an evaluation dataset."""

    def __init__(self) -> None:
        self._recall = RecallAtK()
        self._precision = PrecisionAtK()
        self._mrr = MeanReciprocalRank()
        self._ndcg = NDCGAtK()

    def evaluate(
        self,
        evaluations: list[RetrievalEvaluationResult],
        k: int,
    ) -> RetrievalMetrics:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        recall_scores = [
            self._recall.calculate(evaluation, k)
            for evaluation in evaluations
        ]

        precision_scores = [
            self._precision.calculate(evaluation, k)
            for evaluation in evaluations
        ]

        ndcg_scores = [
            self._ndcg.calculate(evaluation, k)
            for evaluation in evaluations
        ]

        return RetrievalMetrics(
            recall_at_k=self._average(recall_scores),
            precision_at_k=self._average(precision_scores),
            mrr=self._mrr.calculate(evaluations, k),
            ndcg_at_k=self._average(ndcg_scores),
        )

    @staticmethod
    def _average(values: list[float]) -> float:
        if not values:
            return 0.0

        return sum(values) / len(values)