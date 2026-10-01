from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.models.retrieval import RetrievalFilter, RetrievalQuery


def test_retrieval_query_without_filters():
    request = RetrievalQuery(
        query="What is our refund policy?",
    )

    assert request.query == "What is our refund policy?"
    assert request.top_k == 5
    assert request.filters is None


def test_retrieval_query_with_filters():
    document_id = uuid4()

    request = RetrievalQuery(
        query="What is our refund policy?",
        top_k=10,
        filters=RetrievalFilter(
            source="filesystem",
            document_id=document_id,
            document_type="policy",
        ),
    )

    assert request.filters is not None
    assert request.filters.source == "filesystem"
    assert request.filters.document_id == document_id
    assert request.filters.document_type == "policy"


def test_retrieval_filter_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        RetrievalFilter(
            source="filesystem",
            status="active",
        )


def test_retrieval_query_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        RetrievalQuery(
            query="test",
            source="filesystem",
        )


def test_retrieval_query_rejects_invalid_top_k():
    with pytest.raises(ValidationError):
        RetrievalQuery(
            query="test",
            top_k=0,
        )
