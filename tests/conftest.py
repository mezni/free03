import pytest
import uuid
from datetime import datetime


@pytest.fixture
def fixture_period_entity_create_valid():
    """Fixture with Period example"""
    period_code = uuid.uuid4()
    period_date = datetime(2024, 4, 20)
    return {
        "period_code": period_code,
        "period_name": period_date.strftime("%Y-%m-%d"),
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
