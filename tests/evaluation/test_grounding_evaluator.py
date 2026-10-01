from src.evaluation.grounding.evaluator import GroundingEvaluator
from src.models.rag import Citation, RAGResponse


def _response(
    answer: str,
    retrieved_count: int,
    citation_count: int,
) -> RAGResponse:
    return RAGResponse(
        query="What is the billing dispute policy?",
        answer=answer,
        citations=[
            Citation(
                citation_id=f"SOURCE-{index + 1}",
                document_id="doc-1",
                chunk_id=f"chunk-{index + 1}",
                chunk_index=index,
            )
            for index in range(citation_count)
        ],
        model_name="test-model",
        retrieved_count=retrieved_count,
    )


class TestGroundingEvaluator:
    def test_answer_with_citation_is_grounded(self) -> None:
        score = GroundingEvaluator().evaluate(
            _response(
                answer="Customers can dispute billing charges.",
                retrieved_count=3,
                citation_count=1,
            )
        )

        assert score == 1.0

    def test_answer_without_citation_is_not_grounded(self) -> None:
        score = GroundingEvaluator().evaluate(
            _response(
                answer="Customers can dispute billing charges.",
                retrieved_count=3,
                citation_count=0,
            )
        )

        assert score == 0.0

    def test_empty_answer_is_not_grounded(self) -> None:
        score = GroundingEvaluator().evaluate(
            _response(
                answer="",
                retrieved_count=3,
                citation_count=1,
            )
        )

        assert score == 0.0

    def test_whitespace_answer_is_not_grounded(self) -> None:
        score = GroundingEvaluator().evaluate(
            _response(
                answer="   \n  ",
                retrieved_count=3,
                citation_count=1,
            )
        )

        assert score == 0.0

    def test_no_retrieved_context_is_not_grounded(self) -> None:
        score = GroundingEvaluator().evaluate(
            _response(
                answer="Customers can dispute billing charges.",
                retrieved_count=0,
                citation_count=1,
            )
        )

        assert score == 0.0
