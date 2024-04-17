import pytest
from src.entities.resource_entity import Resource


def test_entity_resource_create(fixture_resource_create):
    resource = Resource(
        resource_id=fixture_resource_create["resource_id"],
        name=fixture_resource_create["name"],
    )

    assert resource.resource_id == fixture_resource_create["resource_id"]
    assert resource.name == fixture_resource_create["name"]
