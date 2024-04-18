import pytest
from src.entities.entities import Usage


def test_usage_entity_create_success(fixture_usage_entity_create_success):
    usage = Usage(
        usage_code=fixture_usage_entity_create_success["usage_code"],
        resource_code=fixture_usage_entity_create_success["resource_code"],
        usage_amount=fixture_usage_entity_create_success["usage_amount"],
        usage_currency=fixture_usage_entity_create_success["usage_currency"],
    )
    assert usage.usage_code == fixture_usage_entity_create_success["usage_code"]
    assert usage.resource_code == fixture_usage_entity_create_success["resource_code"]
    assert usage.usage_amount == fixture_usage_entity_create_success["usage_amount"]
    assert usage.usage_currency == fixture_usage_entity_create_success["usage_currency"]


def test_usage_entity_from_dict(fixture_usage_entity_create_success):
    usage = Usage.from_dict(fixture_usage_entity_create_success)
    assert usage.usage_code == fixture_usage_entity_create_success["usage_code"]
    assert usage.resource_code == fixture_usage_entity_create_success["resource_code"]
    assert usage.usage_amount == fixture_usage_entity_create_success["usage_amount"]
    assert usage.usage_currency == fixture_usage_entity_create_success["usage_currency"]


def test_usage_entity_to_dict(fixture_usage_entity_create_success):
    usage = Usage.from_dict(fixture_usage_entity_create_success)
    assert usage.to_dict() == fixture_usage_entity_create_success


def test_usage_entity_comparaison(fixture_usage_entity_create_success):
    usage1 = Usage.from_dict(fixture_usage_entity_create_success)
    usage2 = Usage.from_dict(fixture_usage_entity_create_success)
    assert usage1.to_dict() == usage2.to_dict()
