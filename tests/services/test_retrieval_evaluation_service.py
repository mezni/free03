from uuid import uuid4

from src.models.retrieval import RetrievalResult
from src.models.retrieval_evaluation import (
    EvaluationChunkReference,
    RetrievalEvaluationCase,
)
from src.services.retrieval_evaluation_service import RetrievalEvaluationService

DOC = "data/raw/billing/sample-policy.md"


def make_reference(
    document: str,
    chunk_index: int,
):
    return EvaluationChunkReference(
        document=document,
        chunk_index=chunk_index,
    )


class FakeEvaluationResolver:
    def __init__(self, resolved_ids):
        self.resolved_ids = resolved_ids
        self.references = []

    def resolve_all(self, references):
        self.references.append(references)
        return self.resolved_ids


def make_result(chunk_id):
    return RetrievalResult(
        chunk_id=chunk_id,
        document_id=uuid4(),
        index_version_id=uuid4(),
        content="example",
        chunk_index=0,
        score=0.1,
        retrieval_method="vector",
    )


def test_evaluate_case():
    relevant_reference = make_reference(
        document=DOC,
        chunk_index=0,
    )

    chunk_a = uuid4()
    chunk_b = uuid4()
    resolved_id = uuid4()

    case = RetrievalEvaluationCase(
        case_id="refund-001",
        query="What is the refund policy?",
        relevant_chunks=[
            relevant_reference,
        ],
    )

    results = [
        make_result(chunk_a),
        make_result(chunk_b),
    ]

    resolver = FakeEvaluationResolver(
        resolved_ids=[resolved_id],
    )

    service = RetrievalEvaluationService(
        evaluation_resolver=resolver,
    )

    evaluation = service.evaluate_case(
        case=case,
        results=results,
    )

    assert evaluation.case_id == "refund-001"

    assert evaluation.retrieved_chunk_ids == [
        chunk_a,
        chunk_b,
    ]

    assert evaluation.relevant_chunk_ids == [
        resolved_id,
    ]

    assert resolver.references == [
        [relevant_reference],
    ]
