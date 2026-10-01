from uuid import uuid4

from src.generation.context_builder import ContextBuilder
from src.models.retrieval import RetrievalResult


def make_result(chunk_index: int, content: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        index_version_id=uuid4(),
        content=content,
        chunk_index=chunk_index,
        score=0.5,
        retrieval_method="vector",
    )


def test_build_returns_empty_string_for_no_results():
    assert ContextBuilder().build([]) == ""


def test_build_includes_provenance_and_content():
    result = make_result(3, "Refunds are issued within 5 days.")

    context = ContextBuilder().build([result])

    assert str(result.document_id) in context
    assert "Chunk: 3" in context
    assert "Refunds are issued within 5 days." in context


def test_build_preserves_result_order():
    first = make_result(0, "first content")
    second = make_result(1, "second content")

    context = ContextBuilder().build([first, second])

    assert context.index("first content") < context.index(
        "second content"
    )


def test_build_separates_sections():
    first = make_result(0, "first content")
    second = make_result(1, "second content")

    context = ContextBuilder().build([first, second])

    assert "\n\n" in context
    assert context.count("Chunk:") == 2
