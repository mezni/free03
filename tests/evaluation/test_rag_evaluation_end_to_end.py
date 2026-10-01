"""End-to-end check of the RAG evaluation stack.

Exercises the real dataset loader, runner, service, and all three real
evaluators against the shipped `data/evaluation/rag_v1.yaml`, with only
the RAGService replaced. No network, no database.
"""

from src.evaluation.answer.semantic import SimpleAnswerEvaluator
from src.evaluation.citation.evaluator import CitationEvaluator
from src.evaluation.grounding.evaluator import GroundingEvaluator
from src.evaluation.rag_dataset_loader import (
    RAGEvaluationDatasetLoader,
)
from src.evaluation.rag_evaluation_runner import (
    RAGEvaluationRunner,
)
from src.models.rag import Citation, RAGResponse
from src.services.rag_evaluation_service import RAGEvaluationService

DATASET = "data/evaluation/rag_v1.yaml"


class ScriptedRAGService:
    """Returns a canned response per query, recording the queries seen."""

    def __init__(self, responses: dict[str, RAGResponse]) -> None:
        self._responses = responses
        self.queries: list[str] = []

    def answer(self, query) -> RAGResponse:
        self.queries.append(query.query)

        return self._responses[query.query]


def _cited(answer: str, retrieved_count: int = 3) -> RAGResponse:
    return RAGResponse(
        query="",
        answer=answer,
        citations=[
            Citation(
                citation_id="SOURCE-1",
                document_id="doc-1",
                chunk_id="chunk-1",
                chunk_index=0,
            )
        ],
        model_name="test-model",
        retrieved_count=retrieved_count,
    )


def _uncited(answer: str, retrieved_count: int = 3) -> RAGResponse:
    return RAGResponse(
        query="",
        answer=answer,
        citations=[],
        model_name="test-model",
        retrieved_count=retrieved_count,
    )


def _service(rag_service) -> RAGEvaluationService:
    return RAGEvaluationService(
        rag_service=rag_service,
        answer_evaluator=SimpleAnswerEvaluator(),
        citation_evaluator=CitationEvaluator(),
        grounding_evaluator=GroundingEvaluator(),
    )


class TestRAGEvaluationEndToEnd:
    def test_perfect_answers_score_one_across_the_board(self) -> None:
        _, cases = RAGEvaluationDatasetLoader().load(DATASET)

        # Answer each query with its own reference answer verbatim,
        # correctly cited as SOURCE-1.
        rag_service = ScriptedRAGService(
            {case.query: _cited(case.reference_answer) for case in cases}
        )

        version, metrics = RAGEvaluationRunner(
            dataset_loader=RAGEvaluationDatasetLoader(),
            evaluation_service=_service(rag_service),
        ).run(DATASET)

        assert version == 1
        assert metrics.answer_relevance == 1.0
        assert metrics.citation_precision == 1.0
        assert metrics.citation_recall == 1.0
        assert metrics.grounding == 1.0

    def test_all_metrics_zero_when_nothing_is_cited(self) -> None:
        _, cases = RAGEvaluationDatasetLoader().load(DATASET)

        rag_service = ScriptedRAGService(
            {case.query: _uncited("Kubernetes deployment pipeline overview.") for case in cases}
        )

        _, metrics = RAGEvaluationRunner(
            dataset_loader=RAGEvaluationDatasetLoader(),
            evaluation_service=_service(rag_service),
        ).run(DATASET)

        assert metrics.answer_relevance < 0.2
        assert metrics.citation_precision == 0.0
        assert metrics.citation_recall == 0.0
        assert metrics.grounding == 0.0

    def test_grounding_zero_when_nothing_was_retrieved(self) -> None:
        _, cases = RAGEvaluationDatasetLoader().load(DATASET)

        rag_service = ScriptedRAGService(
            {
                case.query: _cited(
                    case.reference_answer,
                    retrieved_count=0,
                )
                for case in cases
            }
        )

        _, metrics = RAGEvaluationRunner(
            dataset_loader=RAGEvaluationDatasetLoader(),
            evaluation_service=_service(rag_service),
        ).run(DATASET)

        # Citations are structurally present and correct, so citation
        # scores stay high even though nothing was actually retrieved.
        assert metrics.citation_precision == 1.0
        assert metrics.grounding == 0.0

    def test_every_dataset_query_is_answered(self) -> None:
        _, cases = RAGEvaluationDatasetLoader().load(DATASET)

        rag_service = ScriptedRAGService(
            {case.query: _cited(case.reference_answer) for case in cases}
        )

        _service(rag_service).evaluate(cases)

        assert rag_service.queries == [case.query for case in cases]
