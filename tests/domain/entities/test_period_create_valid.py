import pytest
from src.domain.entities.period import Period


def test_period_create_valid(fixture_period_entity_create_valid):
    period = Period(
        period_code=fixture_period_entity_create_valid["period_code"],
        period_name=fixture_period_entity_create_valid["period_name"],
        period_date=fixture_period_entity_create_valid["period_date"],
        period_day=fixture_period_entity_create_valid["period_day"],
        period_month=fixture_period_entity_create_valid["period_month"],
        period_year=fixture_period_entity_create_valid["period_year"],
        period_quarter=fixture_period_entity_create_valid["period_quarter"],
        period_day_of_week=fixture_period_entity_create_valid["period_day_of_week"],
        period_day_of_year=fixture_period_entity_create_valid["period_day_of_year"],
        period_week_of_year=fixture_period_entity_create_valid["period_week_of_year"],
        period_is_holiday=fixture_period_entity_create_valid["period_is_holiday"],
    )
    assert period.period_code == fixture_period_entity_create_valid["period_code"]
    assert period.period_name == fixture_period_entity_create_valid["period_name"]
    assert period.period_date == fixture_period_entity_create_valid["period_date"]
    assert period.period_day == fixture_period_entity_create_valid["period_day"]
    assert period.period_month == fixture_period_entity_create_valid["period_month"]
    assert period.period_year == fixture_period_entity_create_valid["period_year"]
    assert period.period_quarter == fixture_period_entity_create_valid["period_quarter"]
    assert (
        period.period_day_of_week
        == fixture_period_entity_create_valid["period_day_of_week"]
    )
    assert (
        period.period_day_of_year
        == fixture_period_entity_create_valid["period_day_of_year"]
    )
    assert (
        period.period_week_of_year
        == fixture_period_entity_create_valid["period_week_of_year"]
    )
    assert (
        period.period_is_holiday
        == fixture_period_entity_create_valid["period_is_holiday"]
    )
