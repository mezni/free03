from src.core.domain import value_objects as v
from src.core.domain import usage as u


def test_usage_model_init():
    code = v.code
    usage = u.Usage(usage_id=code,org_id='0661be46-fbd3-79c8-8000-2bf97fb86332')
    assert usage.usage_id == code


def test_usage_model_from_dict():
    code = v.code
    usage = u.Usage.from_dict({
            'usage_id': code,'org_id': '0661be46-fbd3-79c8-8000-2bf97fb86332'})
    assert usage.usage_id == code
    
def test_usage_model_to_dict():
    usage_dict =  {
       'usage_id': v.code,
       'org_id': '0661be46-fbd3-79c8-8000-2bf97fb86332',
    } 
    usage = u.Usage.from_dict(usage_dict)
    assert usage.to_dict() == usage_dict
    
