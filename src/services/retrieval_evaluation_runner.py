from src.models.retrieval import RetrievalQuery
from src.models.retrieval_evaluation import (
    RetrievalEvaluationCase,
    RetrievalEvaluationResult,
)
from src.models.retrieval_metrics import RetrievalMetrics
from src.services.evaluation_resolver import EvaluationResolver
from src.services.retrieval_metrics_service import (
    RetrievalMetricsService,
)


class RetrievalEvaluationRunner:
    """Run retrieval evaluation cases against the retrieval pipeline."""

    def __init__(
        self,
        retrieval_pipeline,
        metrics_service: RetrievalMetricsService,
        evaluation_resolver: EvaluationResolver,
    ) -> None:
        self._retrieval_pipeline = retrieval_pipeline
        self._metrics_service = metrics_service
        self._evaluation_resolver = evaluation_resolver

    def evaluate(
        self,
        cases: list[RetrievalEvaluationCase],
        k: int,
    ) -> RetrievalMetrics:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        evaluations: list[RetrievalEvaluationResult] = []
        context_chunk_ids: list[list[str]] = []

        for case in cases:
            evaluation, context_ids = self._evaluate_case(case, k)

            evaluations.append(evaluation)
            context_chunk_ids.append(context_ids)

        return self._metrics_service.evaluate(
            evaluations=evaluations,
            k=k,
            context_chunk_ids=context_chunk_ids,
        )

    def _evaluate_case(
        self,
        case: RetrievalEvaluationCase,
        k: int,
    ) -> tuple[RetrievalEvaluationResult, list[str]]:
        request = RetrievalQuery(
            query=case.query,
            top_k=k,
        )

        results = self._retrieval_pipeline.execute(request)

        relevant_chunk_ids = (
            self._evaluation_resolver.resolve_all(
                case.relevant_chunks
            )
        )

        evaluation = RetrievalEvaluationResult(
            case_id=case.case_id,
            retrieved_chunk_ids=[
                result.chunk_id
                for result in results
            ],
            relevant_chunk_ids=relevant_chunk_ids,
        )

        return evaluation, [
            str(result.chunk_id) for result in results
        ]