import uuid
from costs.domain.resource import Resource

def test_resource_model_init():
    code = str(uuid.uuid4())
    resource = Resource(code=code, name="")
    assert resource.code == code
    assert resource.name == ""