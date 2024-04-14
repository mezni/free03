from src.core.v1.domain import value_objects as v
from src.core.v1.domain import usage as u


def test_usage_model_init():
    code = v.code
    usage = u.Usage(
        usage_id=code,
        resource_id="0661be9f-0260-7f5d-8000-6a4da3317708",
        period="2024-04-14",
        usage_amount=0.013,
        usage_currency="USD",
    )
    assert usage.usage_id == code
    assert usage.resource_id == "0661be9f-0260-7f5d-8000-6a4da3317708"
    assert usage.period == "2024-04-14"
    assert usage.usage_amount == 0.013
    assert usage.usage_currency == "USD"


def test_usage_model_from_dict():
    code = v.code
    usage = u.Usage.from_dict(
        {
            "usage_id": code,
            "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
            "period": "2024-04-14",
            "usage_amount": 0.013,
            "usage_currency": "USD",
        }
    )
    assert usage.usage_id == code
    assert usage.resource_id == "0661be9f-0260-7f5d-8000-6a4da3317708"
    assert usage.period == "2024-04-14"
    assert usage.usage_amount == 0.013
    assert usage.usage_currency == "USD"


def test_usage_model_to_dict():
    usage_dict = {
        "usage_id": v.code,
        "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
        "period": "2024-04-14",
        "usage_amount": 0.013,
        "usage_currency": "USD",
    }
    usage = u.Usage.from_dict(usage_dict)
    assert usage.to_dict() == usage_dict


def test_usage_model_comparaison():
    usage_dict = {
        "usage_id": v.code,
        "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
        "period": "2024-04-14",
        "usage_amount": 0.013,
        "usage_currency": "USD",
    }
    usage1 = u.Usage.from_dict(usage_dict)
    usage2 = u.Usage.from_dict(usage_dict)
    assert usage1 == usage2
