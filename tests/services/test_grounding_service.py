from src.services.grounding_service import GroundingService


def test_answer_with_citation_is_grounded():
    result = GroundingService().validate(
        answer="Disputes take 30 days. [SOURCE-1]",
        citation_count=1,
    )

    assert result.grounded is True
    assert result.citation_count == 1


def test_empty_answer_is_not_grounded():
    result = GroundingService().validate(
        answer="",
        citation_count=0,
    )

    assert result.grounded is False
    assert result.citation_count == 0


def test_whitespace_answer_is_not_grounded():
    result = GroundingService().validate(
        answer="   \n  ",
        citation_count=0,
    )

    assert result.grounded is False


def test_answer_without_citation_is_not_grounded():
    result = GroundingService().validate(
        answer="Disputes take 30 days.",
        citation_count=0,
    )

    assert result.grounded is False


def test_answer_with_citation_reports_count():
    result = GroundingService().validate(
        answer="A [SOURCE-1] B [SOURCE-2]",
        citation_count=2,
    )

    assert result.grounded is True
    assert result.citation_count == 2
