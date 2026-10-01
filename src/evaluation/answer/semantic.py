import re

from src.evaluation.answer.base import AnswerEvaluator
from src.models.rag import RAGResponse
from src.models.rag_evaluation import RAGEvaluationCase


class SimpleAnswerEvaluator(AnswerEvaluator):

    def evaluate(
        self,
        case: RAGEvaluationCase,
        response: RAGResponse,
    ) -> float:
        expected_tokens = self._tokens(
            case.reference_answer
        )

        actual_tokens = self._tokens(
            response.answer
        )

        if not expected_tokens:
            return 0.0

        overlap = (
            expected_tokens & actual_tokens
        )

        return len(overlap) / len(expected_tokens)

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token.lower()
            for token in re.findall(
                r"\b\w+\b",
                text,
            )
        }