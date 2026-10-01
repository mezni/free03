from src.evaluation.answer.base import AnswerEvaluator
from src.evaluation.citation.evaluator import CitationEvaluator
from src.evaluation.grounding.evaluator import GroundingEvaluator
from src.models.rag_evaluation import (
    RAGEvaluationCase,
    RAGEvaluationMetrics,
    RAGEvaluationResult,
)
from src.models.retrieval import RetrievalQuery
from src.services.rag_service import RAGService


class RAGEvaluationService:
    def __init__(
        self,
        rag_service: RAGService,
        answer_evaluator: AnswerEvaluator,
        citation_evaluator: CitationEvaluator,
        grounding_evaluator: GroundingEvaluator,
    ) -> None:
        self._rag_service = rag_service
        self._answer_evaluator = answer_evaluator
        self._citation_evaluator = citation_evaluator
        self._grounding_evaluator = grounding_evaluator

    def evaluate_case(
        self,
        case: RAGEvaluationCase,
    ) -> RAGEvaluationResult:
        response = self._rag_service.answer(
            RetrievalQuery(
                query=case.query,
            )
        )

        answer_relevance = self._answer_evaluator.evaluate(
            case,
            response,
        )

        citation_precision, citation_recall = self._citation_evaluator.evaluate(
            case,
            response,
        )

        grounding = self._grounding_evaluator.evaluate(
            response,
        )

        return RAGEvaluationResult(
            case_id=case.case_id,
            answer_relevance=answer_relevance,
            citation_precision=citation_precision,
            citation_recall=citation_recall,
            grounding=grounding,
        )

    def evaluate(
        self,
        cases: list[RAGEvaluationCase],
    ) -> RAGEvaluationMetrics:
        if not cases:
            raise ValueError("At least one evaluation case is required.")

        results = [self.evaluate_case(case) for case in cases]

        count = len(results)

        return RAGEvaluationMetrics(
            answer_relevance=sum(result.answer_relevance for result in results) / count,
            citation_precision=sum(result.citation_precision for result in results) / count,
            citation_recall=sum(result.citation_recall for result in results) / count,
            grounding=sum(result.grounding for result in results) / count,
        )
