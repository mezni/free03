import pytest
import uuid


@pytest.fixture
def fixture_resource_create():
    """Fixture fixture_resource_create"""
    return {
        "resource_id": uuid.UUID("0661be9f-0260-7f5d-8000-6a4da3317708"),
        "name": "i-127777",
    }
