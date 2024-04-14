import json
from src.core.v1.domain import value_objects as v
from src.core.v1.domain import usage as u
from src.core.v1.serializers import usage_json_serializer as ser


def test_usage_serializer():
    code = v.code
    usage = u.Usage(
        usage_id=code,
        resource_id="0661be9f-0260-7f5d-8000-6a4da3317708",
        period="2024-04-14",
        usage_amount=0.013,
        usage_currency="USD",
    )

    expected_json = """
    {{
        "usage_id": "{}",
        "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
        "period": "2024-04-14",
        "usage_amount": 0.013,
        "usage_currency": "USD"
    }}
    """.format(
        code
    )

    json_usage = json.dumps(usage, cls=ser.UsageJsonEncoder)
    assert json.loads(json_usage) == json.loads(expected_json)
