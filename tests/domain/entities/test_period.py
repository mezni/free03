from src.domain.entities.period import Period


def test_period_creation(fixture_period_success):
    period = Period(
        period_code=fixture_period_success["period_code"],
        period_name=fixture_period_success["period_name"],
    )
    assert period.period_code == fixture_period_success["period_code"]
    assert period.period_name == fixture_period_success["period_name"]


def test_period_from_dict(fixture_period_success):
    period = Period.from_dict(fixture_period_success)
    assert period.period_code == fixture_period_success["period_code"]
    assert period.period_name == fixture_period_success["period_name"]


def test_period_to_dict(fixture_period_success):
    period = Period.from_dict(fixture_period_success)
    assert period.to_dict() == fixture_period_success


def test_period_comparison(fixture_period_success):
    period1 = Period.from_dict(fixture_period_success)
    period2 = Period.from_dict(fixture_period_success)
    assert period1 == period2
