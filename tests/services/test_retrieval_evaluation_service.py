from uuid import uuid4

from src.models.retrieval import RetrievalResult
from src.models.retrieval_evaluation import RetrievalEvaluationCase
from src.services.retrieval_evaluation_service import RetrievalEvaluationService


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
    relevant_chunk_id = uuid4()
    irrelevant_chunk_id = uuid4()

    case = RetrievalEvaluationCase(
        case_id="refund-001",
        query="What is the refund policy?",
        relevant_chunk_ids=[
            relevant_chunk_id,
        ],
    )

    results = [
        make_result(relevant_chunk_id),
        make_result(irrelevant_chunk_id),
    ]

    service = RetrievalEvaluationService()

    evaluation = service.evaluate_case(
        case=case,
        results=results,
    )

    assert evaluation.case_id == "refund-001"

    assert evaluation.retrieved_chunk_ids == [
        relevant_chunk_id,
        irrelevant_chunk_id,
    ]

    assert evaluation.relevant_chunk_ids == [
        relevant_chunk_id,
    ]