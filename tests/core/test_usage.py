from src.core.domain import value_objects as v
from src.core.domain import usage as u

def test_usage_model_init():
    code = v.code
    usage = u.Usage(usage_id=code)
    assert usage.usage_id == code
    