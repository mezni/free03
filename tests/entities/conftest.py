import pytest
import uuid
from src.entities.entities import Usage
from src.entities.entities import Resource


@pytest.fixture
def fixture_usage_entity_create_success():
    """Fixture with Usage"""
    return {
        "usage_code": uuid.UUID("54f7b14f-5cb7-4d8a-bbcd-05627f5bccd3"),
        "resource_code": uuid.UUID("6c6d6cd8-a8d9-4bf1-914a-7581f9c33723"),
        "usage_amount": 0.013,
        "usage_currency": "USD",
    }


@pytest.fixture
def fixture_resource_entity_create_success():
    """Fixture with Usage"""
    return {
        "resource_code": uuid.UUID("6c6d6cd8-a8d9-4bf1-914a-7581f9c33723"),
        "resource_id": "i-gw9i3f18hvsfpecp2d5y",
        "resource_name": "dali-instance-small",
    }


@pytest.fixture
def fixture_period_entity_create_success():
    """Fixture with Usage"""
    return {
        "period_code": uuid.UUID("d4ff5d87-8a82-4a16-8b9a-cad2752b10fc"),
        "period": "i-gw9i3f18hvsfpecp2d5y",
    }
