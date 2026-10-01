from src.models.retrieval import RetrievalResult
from src.models.retrieval_evaluation import (
    RetrievalEvaluationCase,
    RetrievalEvaluationResult,
)
from src.services.evaluation_resolver import EvaluationResolver


class RetrievalEvaluationService:
    """
    Builds evaluation results from retrieval output
    and ground-truth evaluation cases.
    """

    def __init__(
        self,
        evaluation_resolver: EvaluationResolver,
    ) -> None:
        self._evaluation_resolver = evaluation_resolver

    def evaluate_case(
        self,
        case: RetrievalEvaluationCase,
        results: list[RetrievalResult],
    ) -> RetrievalEvaluationResult:
        return RetrievalEvaluationResult(
            case_id=case.case_id,
            retrieved_chunk_ids=[
                result.chunk_id
                for result in results
            ],
            relevant_chunk_ids=(
                self._evaluation_resolver.resolve_all(
                    case.relevant_chunks
                )
            ),
        )