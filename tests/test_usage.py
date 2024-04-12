import uuid
from costs.domain import usage as u


def test_usage_model_init():
    code = str(uuid.uuid4())
    usage = u.Usage(code=code, service="", resource="", amount=0)
    assert usage.code == code
    assert usage.service == ""
