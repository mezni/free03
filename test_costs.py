import uuid
from costs import Resource

def test_resource_model_init():
    id = str(uuid.uuid4())
    resource = Resource(id=id, name="")
    assert resource.id == id
    assert resource.name == ""