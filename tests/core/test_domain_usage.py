from src.core.domain import usage as u


def test_usage_model_init(fixture_usage_developer):
    usage = u.Usage(
        usage_id=fixture_usage_developer["usage_id"],
        resource_id=fixture_usage_developer["resource_id"],
        period=fixture_usage_developer["period"],
        usage_amount=fixture_usage_developer["usage_amount"],
        usage_currency=fixture_usage_developer["usage_currency"],
    )
    assert usage.usage_id == fixture_usage_developer["usage_id"]
    assert usage.resource_id == fixture_usage_developer["resource_id"]
    assert usage.period == fixture_usage_developer["period"]
    assert usage.usage_amount == fixture_usage_developer["usage_amount"]
    assert usage.usage_currency == fixture_usage_developer["usage_currency"]

def test_usage_model_from_dict(fixture_usage_developer):
    usage = u.Usage.from_dict(
        fixture_usage_developer
    )
    assert usage.usage_id == fixture_usage_developer["usage_id"]
    assert usage.resource_id == fixture_usage_developer["resource_id"]
    assert usage.period == fixture_usage_developer["period"]
    assert usage.usage_amount == fixture_usage_developer["usage_amount"]
    assert usage.usage_currency == fixture_usage_developer["usage_currency"]
    
def test_usage_model_to_dict(fixture_usage_developer):
    usage = u.Usage.from_dict(fixture_usage_developer)
    assert usage.to_dict() == fixture_usage_developer
    
def test_usage_model_comparaison(fixture_usage_developer):
    usage1 = u.Usage.from_dict(fixture_usage_developer)
    usage2 = u.Usage.from_dict(fixture_usage_developer)
    assert usage1 == usage2