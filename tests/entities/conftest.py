import pytest
import uuid
from src.entities.entities import Usage


@pytest.fixture
def fixture_usage_entity_create_success():
    """Fixture with Usage"""
    return {
        "usage_code": uuid.UUID("54f7b14f-5cb7-4d8a-bbcd-05627f5bccd3"),
        "resource_code": uuid.UUID("6c6d6cd8-a8d9-4bf1-914a-7581f9c33723"),
        "usage_amount": 0.013,
        "usage_currency": "USD",
    }
