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


def test_build_includes_source_marker_and_provenance():
    result = make_result(3, "Refunds are issued within 5 days.")

    context = ContextBuilder().build([result])

    assert "[SOURCE-1]" in context
    assert f"Document ID: {result.document_id}" in context
    assert f"Chunk ID: {result.chunk_id}" in context
    assert "Chunk Index: 3" in context
    assert "Refunds are issued within 5 days." in context


def test_build_numbers_sources_in_result_order():
    first = make_result(0, "first content")
    second = make_result(1, "second content")

    context = ContextBuilder().build([first, second])

    assert context.index("[SOURCE-1]") < context.index("[SOURCE-2]")
    assert context.index("first content") < context.index("second content")


def test_build_separates_sections():
    context = ContextBuilder().build(
        [
            make_result(0, "first content"),
            make_result(1, "second content"),
        ]
    )

    assert "\n\n" in context
    assert context.count("[SOURCE-") == 2
