from src.evaluation.metrics.retrieval import (
    ContextPrecision,
    ContextRecall,
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
        self._context_recall = ContextRecall()
        self._context_precision = ContextPrecision()

    def evaluate(
        self,
        evaluations: list[RetrievalEvaluationResult],
        k: int,
        context_chunk_ids: list[list[str]] | None = None,
    ) -> RetrievalMetrics:
        """Score ranked retrieval, and optionally the final context.

        `context_chunk_ids` is one list of chunk id strings per
        evaluation, in the same order. When omitted, context metrics
        stay None rather than being guessed from the ranked list.
        """
        if k <= 0:
            raise ValueError("k must be greater than 0")

        recall_scores = [self._recall.calculate(evaluation, k) for evaluation in evaluations]

        precision_scores = [self._precision.calculate(evaluation, k) for evaluation in evaluations]

        ndcg_scores = [self._ndcg.calculate(evaluation, k) for evaluation in evaluations]

        context_recall: float | None = None
        context_precision: float | None = None

        if context_chunk_ids is not None:
            if len(context_chunk_ids) != len(evaluations):
                raise ValueError("context_chunk_ids must align with evaluations")

            context_recall = self._average(
                [
                    self._context_recall.calculate(
                        evaluation,
                        chunk_ids,
                    )
                    for evaluation, chunk_ids in zip(
                        evaluations,
                        context_chunk_ids,
                        strict=True,
                    )
                ]
            )

            context_precision = self._average(
                [
                    self._context_precision.calculate(
                        evaluation,
                        chunk_ids,
                    )
                    for evaluation, chunk_ids in zip(
                        evaluations,
                        context_chunk_ids,
                        strict=True,
                    )
                ]
            )

        return RetrievalMetrics(
            recall_at_k=self._average(recall_scores),
            precision_at_k=self._average(precision_scores),
            mrr=self._mrr.calculate(evaluations, k),
            ndcg_at_k=self._average(ndcg_scores),
            context_recall=context_recall,
            context_precision=context_precision,
        )

    @staticmethod
    def _average(values: list[float]) -> float:
        if not values:
            return 0.0

        return sum(values) / len(values)
