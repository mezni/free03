import uuid
from costs.domain import resource as r


def test_resource_model_init():
    code = str(uuid.uuid4())
    resource = r.Resource(code=code, name="")
    assert resource.code == code
    assert resource.name == ""
