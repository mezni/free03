import pytest
from src.core.domain import value_objects as v


@pytest.fixture
def fixture_usage_developer():
    """Fixture with Usage example"""
    return {
        "usage_id": v.code,
        "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
        "period": "2024-04-14",
        "usage_amount": 0.013,
        "usage_currency": "USD",
    }
