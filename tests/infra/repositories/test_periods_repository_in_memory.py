import pytest
from datetime import datetime
from src.domain.entities.period import Period
from src.infra.repositories.periods_repository_in_memory import PeriodInMemoryRepository


def test_periods_repository_in_memory(fixture_period_entity_valid):
    repository = PeriodInMemoryRepository()

    period = repository.create_period(
        fixture_period_entity_valid["period_name"],
    )
    response = repository.get_period_by_name(fixture_period_entity_valid["period_name"])
    assert response.period_name == fixture_period_entity_valid["period_name"]

    periods = repository.create_periods_interval("2024-04-01", "2024-04-30")
    assert len(periods) == 30
    periods = repository.get_periods_periods_interval("2024-04-01", "2024-04-10")
    assert len(periods) == 10
