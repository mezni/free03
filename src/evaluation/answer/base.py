from abc import ABC, abstractmethod

from src.models.rag import RAGResponse
from src.models.rag_evaluation import RAGEvaluationCase


class AnswerEvaluator(ABC):
    @abstractmethod
    def evaluate(
        self,
        case: RAGEvaluationCase,
        response: RAGResponse,
    ) -> float:
        raise NotImplementedError
