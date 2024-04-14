from src.core.domain import value_objects as v
from src.core.domain import usage as u


def test_usage_model_init():
    code = v.code
    usage = u.Usage(
        usage_id=code,
        org_id="0661be46-fbd3-79c8-8000-2bf97fb86332",
        source_id="0661be77-876d-77e8-8000-afffb7a4ab8d",
        provider="aws",
        resource_id="0661be9f-0260-7f5d-8000-6a4da3317708",
        resource_name="i-082b1a163698b8ede",
        period="2024-04-14",
    )
    assert usage.usage_id == code
    assert usage.org_id == "0661be46-fbd3-79c8-8000-2bf97fb86332"
    assert usage.source_id == "0661be77-876d-77e8-8000-afffb7a4ab8d"
    assert usage.provider == "aws"
    assert usage.resource_id == "0661be9f-0260-7f5d-8000-6a4da3317708"
    assert usage.resource_name == "i-082b1a163698b8ede"
    assert usage.period == "2024-04-14"


def test_usage_model_from_dict():
    code = v.code
    usage = u.Usage.from_dict(
        {
            "usage_id": code,
            "org_id": "0661be46-fbd3-79c8-8000-2bf97fb86332",
            "source_id": "0661be77-876d-77e8-8000-afffb7a4ab8d",
            "provider": "aws",
            "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
            "resource_name": "i-082b1a163698b8ede",
            "period": "2024-04-14",
        }
    )
    assert usage.usage_id == code
    assert usage.org_id == "0661be46-fbd3-79c8-8000-2bf97fb86332"
    assert usage.source_id == "0661be77-876d-77e8-8000-afffb7a4ab8d"
    assert usage.provider == "aws"
    assert usage.resource_id == "0661be9f-0260-7f5d-8000-6a4da3317708"
    assert usage.resource_name == "i-082b1a163698b8ede"
    assert usage.period == "2024-04-14"


def test_usage_model_to_dict():
    usage_dict = {
        "usage_id": v.code,
        "org_id": "0661be46-fbd3-79c8-8000-2bf97fb86332",
        "source_id": "0661be77-876d-77e8-8000-afffb7a4ab8d",
        "provider": "aws",
        "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
        "resource_name": "i-082b1a163698b8ede",
        "period": "2024-04-14",
    }
    usage = u.Usage.from_dict(usage_dict)
    assert usage.to_dict() == usage_dict
