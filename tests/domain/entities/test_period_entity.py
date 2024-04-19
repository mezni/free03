from src.domain.entities.period import Period


def test_period_entity_creation_valid(fixture_period_valid):
    period = Period(
        period_code=fixture_period_valid["period_code"],
        period_name=fixture_period_valid["period_name"],
    )
    assert period.period_code == fixture_period_valid["period_code"]
    assert period.period_name == fixture_period_valid["period_name"]


def test_period_from_dict(fixture_period_valid):
    period = Period.from_dict(fixture_period_valid)
    assert period.period_code == fixture_period_valid["period_code"]
    assert period.period_name == fixture_period_valid["period_name"]


def test_period_to_dict(fixture_period_valid):
    period = Period.from_dict(fixture_period_valid)
    assert period.to_dict() == fixture_period_valid


def test_period_comparison(fixture_period_valid):
    period1 = Period.from_dict(fixture_period_valid)
    period2 = Period.from_dict(fixture_period_valid)
    assert period1 == period2
