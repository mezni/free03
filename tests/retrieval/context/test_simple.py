from uuid import uuid4

from src.models.retrieval import RetrievalResult
from src.retrieval.context.simple import SimpleContextSelector


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


def make_results(count: int) -> list[RetrievalResult]:
    return [make_result(f"content {i}") for i in range(count)]


def test_context_selector_limits_results() -> None:
    selector = SimpleContextSelector()

    results = make_results(5)

    selected = selector.select(
        results,
        max_chunks=2,
    )

    assert len(selected) == 2


def test_selector_preserves_rank_order() -> None:
    selector = SimpleContextSelector()

    results = make_results(5)

    selected = selector.select(
        results,
        max_chunks=3,
    )

    assert [r.content for r in selected] == [
        "content 0",
        "content 1",
        "content 2",
    ]


def test_selector_returns_all_when_under_limit() -> None:
    selector = SimpleContextSelector()

    results = make_results(2)

    selected = selector.select(
        results,
        max_chunks=8,
    )

    assert selected == results


def test_selector_returns_empty_for_empty_results() -> None:
    selected = SimpleContextSelector().select(
        [],
        max_chunks=5,
    )

    assert selected == []


def test_selector_returns_empty_for_zero_limit() -> None:
    selected = SimpleContextSelector().select(
        make_results(3),
        max_chunks=0,
    )

    assert selected == []