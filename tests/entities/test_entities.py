import pytest
from src.entities.entities import Usage
from src.entities.entities import Resource
from src.entities.entities import Period


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


def test_resource_entity_create_success(fixture_resource_entity_create_success):
    resource = Resource(
        resource_code=fixture_resource_entity_create_success["resource_code"],
        resource_id=fixture_resource_entity_create_success["resource_id"],
        resource_name=fixture_resource_entity_create_success["resource_name"],
    )
    assert (
        resource.resource_code
        == fixture_resource_entity_create_success["resource_code"]
    )
    assert resource.resource_id == fixture_resource_entity_create_success["resource_id"]
    assert (
        resource.resource_name
        == fixture_resource_entity_create_success["resource_name"]
    )


def test_resource_entity_from_dict(fixture_resource_entity_create_success):
    resource = Resource.from_dict(fixture_resource_entity_create_success)
    assert (
        resource.resource_code
        == fixture_resource_entity_create_success["resource_code"]
    )
    assert resource.resource_id == fixture_resource_entity_create_success["resource_id"]
    assert (
        resource.resource_name
        == fixture_resource_entity_create_success["resource_name"]
    )


def test_resource_entity_to_dict(fixture_resource_entity_create_success):
    resource = Resource.from_dict(fixture_resource_entity_create_success)
    assert resource.to_dict() == fixture_resource_entity_create_success


def test_resource_entity_comparaison(fixture_resource_entity_create_success):
    resource1 = Resource.from_dict(fixture_resource_entity_create_success)
    resource2 = Resource.from_dict(fixture_resource_entity_create_success)
    assert resource1.to_dict() == resource2.to_dict()


def test_period_entity_create_success(fixture_period_entity_create_success):
    period = Period(
        period_code=fixture_period_entity_create_success["period_code"],
        period=fixture_period_entity_create_success["period"],
    )
    assert period.period_code == fixture_period_entity_create_success["period_code"]
    assert period.period == fixture_period_entity_create_success["period"]


def test_period_entity_from_dict(fixture_period_entity_create_success):
    period = Period.from_dict(fixture_period_entity_create_success)
    assert period.period_code == fixture_period_entity_create_success["period_code"]
    assert period.period == fixture_period_entity_create_success["period"]


def test_period_entity_to_dict(fixture_period_entity_create_success):
    period = Period.from_dict(fixture_period_entity_create_success)
    assert period.to_dict() == fixture_period_entity_create_success


def test_period_entity_comparaison(fixture_period_entity_create_success):
    period1 = Period.from_dict(fixture_period_entity_create_success)
    period2 = Period.from_dict(fixture_period_entity_create_success)
    assert period1.to_dict() == period2.to_dict()
