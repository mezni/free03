from uuid import uuid4

import pytest
from sqlalchemy import func, select

from src.db.models.llm_usage import LLMUsageDB
from src.db.repositories.llm_usage import LLMUsageRepository
from src.models.llm_usage import LLMUsageRecord


def make_usage(
    request_id: str | None = None,
    model_name: str = "openai/gpt-oss-20b:free",
    estimated_cost: float = 0.0,
) -> LLMUsageRecord:
    return LLMUsageRecord(
        request_id=request_id,
        provider="openrouter",
        model_name=model_name,
        prompt_tokens=1_000,
        completion_tokens=500,
        total_tokens=1_500,
        estimated_cost=estimated_cost,
        currency="USD",
    )


def test_create_returns_stored_record(database_session) -> None:
    repository = LLMUsageRepository(database_session)

    created = repository.create(make_usage(request_id="req-create"))

    database_session.commit()

    assert created.id is not None
    assert created.created_at is not None
    assert created.request_id == "req-create"


def test_create_persists_columns(database_session) -> None:
    repository = LLMUsageRepository(database_session)

    created = repository.create(make_usage(estimated_cost=0.25))

    database_session.commit()

    stored = repository.get_by_id(created.id)

    assert stored is not None
    assert stored.provider == "openrouter"
    assert stored.model_name == "openai/gpt-oss-20b:free"
    assert stored.prompt_tokens == 1_000
    assert stored.completion_tokens == 500
    assert stored.total_tokens == 1_500
    assert stored.estimated_cost == pytest.approx(0.25)
    assert stored.currency == "USD"


def test_list_by_request_id(database_session) -> None:
    repository = LLMUsageRepository(database_session)

    repository.create(make_usage(request_id="req-multi"))
    repository.create(make_usage(request_id="req-multi"))
    repository.create(make_usage(request_id="req-other"))

    database_session.commit()

    records = repository.list_by_request_id("req-multi")

    assert len(records) == 2
    assert all(record.request_id == "req-multi" for record in records)


def test_get_by_id_returns_none_for_unknown_id(
    database_session,
) -> None:
    repository = LLMUsageRepository(database_session)

    assert repository.get_by_id(uuid4()) is None


def test_usage_rows_are_removed_on_rollback(
    database_session,
) -> None:
    repository = LLMUsageRepository(database_session)

    repository.create(make_usage(request_id="req-rollback"))

    database_session.rollback()

    count = database_session.execute(select(func.count()).select_from(LLMUsageDB)).scalar_one()

    assert count == 0
