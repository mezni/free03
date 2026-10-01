from src.evaluation.citation.evaluator import CitationEvaluator
from src.models.rag import Citation, RAGResponse
from src.models.rag_evaluation import RAGEvaluationCase


def _response(*citation_ids: str) -> RAGResponse:
    return RAGResponse(
        query="What is the billing dispute policy?",
        answer="Customers can dispute billing charges.",
        citations=[
            Citation(
                citation_id=citation_id,
                document_id="doc-1",
                chunk_id=f"chunk-{citation_id}",
                chunk_index=0,
            )
            for citation_id in citation_ids
        ],
        model_name="test-model",
        retrieved_count=len(citation_ids),
    )


def _case(*expected: str) -> RAGEvaluationCase:
    return RAGEvaluationCase(
        case_id="billing-policy-answer-001",
        query="What is the billing dispute policy?",
        reference_answer="Customers can dispute billing charges.",
        expected_citations=list(expected),
    )


class TestCitationEvaluator:
    def test_exact_match_scores_one(self) -> None:
        precision, recall = CitationEvaluator().evaluate(
            _case("SOURCE-1"),
            _response("SOURCE-1"),
        )

        assert precision == 1.0
        assert recall == 1.0

    def test_wrong_citation_scores_zero(self) -> None:
        precision, recall = CitationEvaluator().evaluate(
            _case("SOURCE-1"),
            _response("SOURCE-2"),
        )

        assert precision == 0.0
        assert recall == 0.0

    def test_partial_overlap(self) -> None:
        precision, recall = CitationEvaluator().evaluate(
            _case("SOURCE-1", "SOURCE-2"),
            _response("SOURCE-1"),
        )

        assert precision == 1.0
        assert recall == 0.5

    def test_extra_generated_citation_lowers_precision(self) -> None:
        precision, recall = CitationEvaluator().evaluate(
            _case("SOURCE-1"),
            _response("SOURCE-1", "SOURCE-9"),
        )

        assert precision == 0.5
        assert recall == 1.0

    def test_no_generated_citations_scores_zero(self) -> None:
        precision, recall = CitationEvaluator().evaluate(
            _case("SOURCE-1"),
            _response(),
        )

        assert precision == 0.0
        assert recall == 0.0

    def test_no_expectations_and_no_citations_is_perfect(self) -> None:
        precision, recall = CitationEvaluator().evaluate(
            _case(),
            _response(),
        )

        assert precision == 1.0
        assert recall == 1.0

    def test_no_expectations_but_generated_citation_is_imprecise(
        self,
    ) -> None:
        precision, recall = CitationEvaluator().evaluate(
            _case(),
            _response("SOURCE-1"),
        )

        assert precision == 0.0
        assert recall == 1.0
