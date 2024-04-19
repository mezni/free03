import pytest
import uuid


@pytest.fixture
def fixture_period_success():
    """Fixture with Usage example"""
    period_code = uuid.uuid4()
    return {"period_code": period_code, "period_name": "2024-04-01"}
