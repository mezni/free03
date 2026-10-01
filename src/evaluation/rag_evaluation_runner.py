from src.evaluation.rag_dataset_loader import (
    RAGEvaluationDatasetLoader,
)
from src.models.rag_evaluation import RAGEvaluationMetrics
from src.services.rag_evaluation_service import (
    RAGEvaluationService,
)


class RAGEvaluationRunner:
    def __init__(
        self,
        dataset_loader: RAGEvaluationDatasetLoader,
        evaluation_service: RAGEvaluationService,
    ) -> None:
        self._dataset_loader = dataset_loader
        self._evaluation_service = evaluation_service

    def run(
        self,
        dataset_path: str,
    ) -> tuple[int, RAGEvaluationMetrics]:
        version, cases = self._dataset_loader.load(dataset_path)

        metrics = self._evaluation_service.evaluate(cases)

        return version, metrics
