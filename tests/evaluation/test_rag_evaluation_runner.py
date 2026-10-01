from src.evaluation.rag_dataset_loader import (
    RAGEvaluationDatasetLoader,
)
from src.evaluation.rag_evaluation_runner import (
    RAGEvaluationRunner,
)
from src.models.rag_evaluation import RAGEvaluationMetrics


class FakeLoader:
    def __init__(self, version, cases) -> None:
        self._version = version
        self._cases = cases
        self.paths: list[str] = []

    def load(self, path):
        self.paths.append(path)

        return self._version, self._cases


class FakeEvaluationService:
    def __init__(self, metrics) -> None:
        self._metrics = metrics
        self.batches: list[list] = []

    def evaluate(self, cases):
        self.batches.append(cases)

        return self._metrics


class TestRAGEvaluationRunner:
    def test_returns_version_and_metrics(self) -> None:
        metrics = RAGEvaluationMetrics(
            answer_relevance=0.5,
            citation_precision=1.0,
            citation_recall=0.5,
            grounding=1.0,
        )

        runner = RAGEvaluationRunner(
            dataset_loader=FakeLoader(1, ["case"]),
            evaluation_service=FakeEvaluationService(
                metrics
            ),
        )

        version, result = runner.run("data/evaluation/rag_v1.yaml")

        assert version == 1
        assert result is metrics

    def test_passes_loaded_cases_to_service(self) -> None:
        metrics = RAGEvaluationMetrics(
            answer_relevance=0.0,
            citation_precision=0.0,
            citation_recall=0.0,
            grounding=0.0,
        )

        loader = FakeLoader(3, ["case-a", "case-b"])
        service = FakeEvaluationService(metrics)

        RAGEvaluationRunner(
            dataset_loader=loader,
            evaluation_service=service,
        ).run("custom.yaml")

        assert loader.paths == ["custom.yaml"]
        assert service.batches == [["case-a", "case-b"]]


class TestRealRunnerComposition:
    def test_runs_shipped_dataset_with_stub_service(
        self,
    ) -> None:
        """Loader and runner compose without touching the database."""

        class StubService:
            def evaluate(self, cases):
                return RAGEvaluationMetrics(
                    answer_relevance=1.0,
                    citation_precision=1.0,
                    citation_recall=1.0,
                    grounding=1.0,
                )

        version, metrics = RAGEvaluationRunner(
            dataset_loader=RAGEvaluationDatasetLoader(),
            evaluation_service=StubService(),
        ).run("data/evaluation/rag_v1.yaml")

        assert version == 1
        assert metrics.answer_relevance == 1.0