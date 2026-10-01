from uuid import uuid4

from src.generation.prompt_builder import PromptBuilder
from src.models.retrieval import RetrievalResult


def make_result(content: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        index_version_id=uuid4(),
        content=content,
        chunk_index=0,
        score=0.5,
        retrieval_method="vector",
    )


def test_system_prompt_instructs_citation_format():
    system_prompt = PromptBuilder().build_system_prompt()

    assert "[SOURCE-N]" in system_prompt
    assert "only the supplied sources" in system_prompt
    assert "insufficient" in system_prompt


def test_prompt_contains_sources():
    results = [make_result("Billing disputes are filed within 30 days.")]

    user_prompt = PromptBuilder().build_user_prompt(
        query="What is the billing policy?",
        results=results,
    )

    assert "[SOURCE-1]" in user_prompt

    assert (
        "Billing disputes are filed within 30 days."
        in user_prompt
    )


def test_prompt_contains_question():
    results = [make_result("content")]

    user_prompt = PromptBuilder().build_user_prompt(
        query="What is the billing policy?",
        results=results,
    )

    assert "Question:\nWhat is the billing policy?" in user_prompt


def test_prompt_numbers_sources_in_result_order():
    first = make_result("first content")
    second = make_result("second content")

    user_prompt = PromptBuilder().build_user_prompt(
        query="query",
        results=[first, second],
    )

    assert user_prompt.index("[SOURCE-1]") < user_prompt.index(
        "[SOURCE-2]"
    )

    assert user_prompt.index("first content") < user_prompt.index(
        "second content"
    )


def test_prompt_has_no_sources_for_no_results():
    user_prompt = PromptBuilder().build_user_prompt(
        query="query",
        results=[],
    )

    assert "[SOURCE-1]" not in user_prompt
