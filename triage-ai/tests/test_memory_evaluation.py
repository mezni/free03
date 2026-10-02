from datetime import datetime, timezone

import pytest

from support_agent.memory_evaluation import (
    evaluate_memory_case,
)
from support_agent.models import (
    EvaluationStatus,
    MemoryEvaluationResult,
    MemorySource,
    MemoryType,
)
from tests.conftest import evaluation_database


def test_evaluate_always_relevant_preference(
    evaluation_database,
):

    from support_agent.evaluation_data import seed_memory_evaluation_data

    seed_memory_evaluation_data()

    service = MemoryService()

    result = evaluate_memory_case(
        name="always_relevant_preference",
        customer_id="C001",
        query="I have a billing problem.",
        expected_memory_key="preferred_contact_method",
    )

    assert result.status == EvaluationStatus.PASS
    assert "preferred_contact_method" in result.details


def test_product_memory_requires_relevance(
    evaluation_database,
):

    from support_agent.evaluation_data import seed_memory_evaluation_data

    seed_memory_evaluation_data()

    service = MemoryService()

    result = evaluate_memory_case(
        name="product_relevance",
        customer_id="C001",
        query="The mobile application crashes.",
        expected_memory_key="product",
    )

    assert result.status == EvaluationStatus.PASS


def test_irrelevant_product_memory_not_returned(
    evaluation_database,
):

    from support_agent.evaluation_data import seed_memory_evaluation_data

    seed_memory_evaluation_data()

    service = MemoryService()

    result = evaluate_memory_case(
        name="irrelevant_product_memory",
        customer_id="C001",
        query="I was charged twice.",
        expected_memory_key=None,
    )

    assert result.status == EvaluationStatus.PASS


def test_memory_evaluation_customer_isolation(
    evaluation_database,
):

    from support_agent.evaluation_data import seed_memory_evaluation_data

    seed_memory_evaluation_data()

    service = MemoryService()

    results = service.retrieve(
        customer_id="C001",
        query="How should you contact me?",
    )

    values = {
        item.memory.value
        for item in results
    }

    assert "email" in values
    assert "phone" not in values


def test_evaluation_result_models():

    from support_agent.models import EvaluationStatus, MemoryEvaluationResult

    # Test PASS result
    pass_result = MemoryEvaluationResult(
        name="test_pass",
        status=EvaluationStatus.PASS,
        details="All good",
    )
    assert pass_result.status == EvaluationStatus.PASS

    # Test FAIL result
    fail_result = MemoryEvaluationResult(
        name="test_fail",
        status=EvaluationStatus.FAIL,
        details="Something went wrong",
    )
    assert fail_result.status == EvaluationStatus.FAIL