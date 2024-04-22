import pytest
from datetime import datetime
from src.domain.entities.period import Period


def test_period_create(fixture_period_entity_valid):
    period_date = datetime.strptime(
        fixture_period_entity_valid["period_name"], "%Y-%m-%d"
    )
    period = Period(
        period_code=fixture_period_entity_valid["period_code"],
        period_name=fixture_period_entity_valid["period_name"],
    )
    assert period.period_code == fixture_period_entity_valid["period_code"]
    assert period.period_name == fixture_period_entity_valid["period_name"]
    assert period.period_date == period_date
    assert period.period_day == period_date.day
    assert period.period_month == period_date.month
    assert period.period_year == period_date.year
    assert period.period_quarter == period_date.month // 3 + 1
    assert period.period_day_of_week == period_date.weekday() + 1
    assert period.period_day_of_year == period_date.timetuple().tm_yday
    assert period.period_week_of_year == period_date.isocalendar()[1]
    assert period.period_is_holiday == False


def test_period_from_dict(fixture_period_entity_valid):
    period = Period.from_dict(fixture_period_entity_valid)
    period_date = datetime.strptime(
        fixture_period_entity_valid["period_name"], "%Y-%m-%d"
    )
    assert period.period_code == fixture_period_entity_valid["period_code"]
    assert period.period_name == fixture_period_entity_valid["period_name"]
    assert period.period_date == period_date
    assert period.period_day == period_date.day
    assert period.period_month == period_date.month
    assert period.period_year == period_date.year
    assert period.period_quarter == period_date.month // 3 + 1
    assert period.period_day_of_week == period_date.weekday() + 1
    assert period.period_day_of_year == period_date.timetuple().tm_yday
    assert period.period_week_of_year == period_date.isocalendar()[1]
    assert period.period_is_holiday == False


def test_period_to_dict(fixture_period_entity_valid):
    period = Period.from_dict(fixture_period_entity_valid)
    period_date = datetime.strptime(
        fixture_period_entity_valid["period_name"], "%Y-%m-%d"
    )
    assert period.to_dict() == {
        "period_code": fixture_period_entity_valid["period_code"],
        "period_name": fixture_period_entity_valid["period_name"],
        "period_date": period_date,
        "period_day": period_date.day,
        "period_month": period_date.month,
        "period_year": period_date.year,
        "period_quarter": period_date.month // 3 + 1,
        "period_day_of_week": period_date.weekday() + 1,
        "period_day_of_year": period_date.timetuple().tm_yday,
        "period_week_of_year": period_date.isocalendar()[1],
        "period_is_holiday": False,
    }


def test_period_comparaison(fixture_period_entity_valid):
    period1 = Period.from_dict(fixture_period_entity_valid)
    period2 = Period.from_dict(fixture_period_entity_valid)
    assert period1 == period2
