import pytest
import uuid
from datetime import datetime


@pytest.fixture
def fixture_period_entity_valid():
    """Fixture with Period example"""
    period_code = uuid.uuid4()
    period_name = "2024-04-20"
    return {"period_code": period_code, "period_name": period_name}
