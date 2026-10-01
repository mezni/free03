from src.models.retrieval import RetrievalResult
from src.models.retrieval_evaluation import (
    RetrievalEvaluationCase,
    RetrievalEvaluationResult,
)


class RetrievalEvaluationService:
    """
    Builds evaluation results from retrieval output
    and ground-truth evaluation cases.
    """

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
            relevant_chunk_ids=case.relevant_chunk_ids,
        )