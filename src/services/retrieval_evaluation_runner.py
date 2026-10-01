from src.models.retrieval import RetrievalQuery
from src.models.retrieval_evaluation import (
    RetrievalEvaluationCase,
    RetrievalEvaluationResult,
)
from src.models.retrieval_metrics import RetrievalMetrics
from src.services.retrieval_metrics_service import RetrievalMetricsService


class RetrievalEvaluationRunner:
    """Run retrieval evaluation cases against the retrieval pipeline."""

    def __init__(
        self,
        retrieval_pipeline,
        metrics_service: RetrievalMetricsService,
    ) -> None:
        self._retrieval_pipeline = retrieval_pipeline
        self._metrics_service = metrics_service

    def evaluate(
        self,
        cases: list[RetrievalEvaluationCase],
        k: int,
    ) -> RetrievalMetrics:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        evaluations = [
            self._evaluate_case(case, k)
            for case in cases
        ]

        return self._metrics_service.evaluate(
            evaluations=evaluations,
            k=k,
        )

    def _evaluate_case(
        self,
        case: RetrievalEvaluationCase,
        k: int,
    ) -> RetrievalEvaluationResult:
        request = RetrievalQuery(
            query=case.query,
            top_k=k,
        )

        results = self._retrieval_pipeline.execute(request)

        return RetrievalEvaluationResult(
            case_id=case.case_id,
            retrieved_chunk_ids=[
                result.chunk_id
                for result in results
            ],
            relevant_chunk_ids=case.relevant_chunk_ids,
        )