from src.models.query_analysis import QueryAnalysis
from src.models.retrieval import RetrievalFilter
from src.retrieval.query.expander import QueryExpander
from src.retrieval.query.simple import SimpleQueryAnalyzer


def test_query_normalization() -> None:
    analyzer = SimpleQueryAnalyzer()

    result = analyzer.analyze(
        "  What   is   the   refund policy?  "
    )

    assert result.original_query == (
        "  What   is   the   refund policy?  "
    )

    assert result.rewritten_query == (
        "What is the refund policy?"
    )


def test_normalization_collapses_newlines_and_tabs() -> None:
    analyzer = SimpleQueryAnalyzer()

    result = analyzer.analyze("refund\n\tpolicy")

    assert result.rewritten_query == "refund policy"


def test_normalization_preserves_clean_query() -> None:
    analyzer = SimpleQueryAnalyzer()

    result = analyzer.analyze("What is the refund policy?")

    assert result.original_query == "What is the refund policy?"
    assert result.rewritten_query == "What is the refund policy?"


def test_baseline_analyzer_sets_no_filters() -> None:
    result = SimpleQueryAnalyzer().analyze("query")

    assert result.filters is None


def test_analysis_is_structured_not_a_string() -> None:
    """The contract is an object, so fields can be added later."""
    analysis = SimpleQueryAnalyzer().analyze("query")

    assert isinstance(analysis, QueryAnalysis)
    assert hasattr(analysis, "original_query")
    assert hasattr(analysis, "rewritten_query")
    assert hasattr(analysis, "filters")


def test_analysis_accepts_filters() -> None:
    analysis = QueryAnalysis(
        original_query="billing policy",
        rewritten_query="billing policy",
        filters=RetrievalFilter(document_type="markdown"),
    )

    assert analysis.filters is not None
    assert analysis.filters.document_type == "markdown"


def test_analysis_rejects_extra_fields() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        QueryAnalysis(
            original_query="q",
            rewritten_query="q",
            intent="informational",
        )


def test_analysis_rejects_empty_rewritten_query() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        QueryAnalysis(
            original_query="q",
            rewritten_query="",
        )


class TestQueryExpander:
    def test_query_expansion_removes_duplicates(self) -> None:
        analyzer = SimpleQueryAnalyzer()
        expander = QueryExpander()

        analysis = analyzer.analyze(
            "What is the refund policy?"
        )

        queries = expander.expand(analysis)

        assert len(queries) == 1

    def test_expansion_keeps_original_when_rewritten_differs(
        self,
    ) -> None:
        expander = QueryExpander()

        analysis = QueryAnalysis(
            original_query="  refund  policy ",
            rewritten_query="refund policy",
        )

        assert expander.expand(analysis) == [
            "  refund  policy ",
            "refund policy",
        ]

    def test_expansion_is_deterministic(self) -> None:
        expander = QueryExpander()

        analysis = SimpleQueryAnalyzer().analyze("a  b")

        first = expander.expand(analysis)
        second = expander.expand(analysis)

        assert first == second