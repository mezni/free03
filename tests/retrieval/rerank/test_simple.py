from uuid import uuid4

from src.models.retrieval import RetrievalResult
from src.retrieval.rerank.simple import SimpleReranker


def make_result(content: str, retrieval_method: str = "vector") -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        index_version_id=uuid4(),
        content=content,
        chunk_index=0,
        score=0.0,
        retrieval_method=retrieval_method,
    )


def test_simple_reranker_preserves_order():
    candidates = [
        make_result("first", "vector"),
        make_result("second", "vector"),
        make_result("third", "vector"),
    ]

    reranker = SimpleReranker()

    results = reranker.rerank(
        query="test",
        candidates=candidates,
        top_k=2,
    )

    assert len(results) == 2
    assert results[0].content == "first"
    assert results[1].content == "second"
    assert results[0].retrieval_method == "reranked"
    assert results[1].retrieval_method == "reranked"


def test_simple_reranker_respects_top_k():
    candidates = [
        make_result("first", "vector"),
        make_result("second", "vector"),
        make_result("third", "vector"),
        make_result("fourth", "vector"),
    ]

    reranker = SimpleReranker()

    results = reranker.rerank(
        query="test",
        candidates=candidates,
        top_k=3,
    )

    assert len(results) == 3
    assert results[0].content == "first"
    assert results[1].content == "second"
    assert results[2].content == "third"
    assert results[0].retrieval_method == "reranked"
    assert results[1].retrieval_method == "reranked"
    assert results[2].retrieval_method == "reranked"


def test_simple_reranker_raises_on_invalid_top_k():
    candidates = [
        make_result("first", "vector"),
    ]

    reranker = SimpleReranker()

    try:
        reranker.rerank(
            query="test",
            candidates=candidates,
            top_k=0,
        )
        raise AssertionError("Expected ValueError")
    except ValueError as e:
        assert "top_k must be greater than zero" in str(e)
