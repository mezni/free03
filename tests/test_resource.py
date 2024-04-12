import uuid
from costs.domain import resource as r


def test_resource_model_init():
    resource_id = str(uuid.uuid4())
    cloud_resource_id = str(uuid.uuid4())
    resource = r.Resource(
        resource_id=resource_id,
        cloud_resource_id=cloud_resource_id,
        resource_name="i-193b1a174798b8ede",
        cloud_type="aws",
    )
    assert resource.resource_id == resource_id
    assert resource.cloud_resource_id == cloud_resource_id
    assert resource.resource_name == "i-193b1a174798b8ede"
    assert resource.cloud_type == "aws"


def test_resource_model_from_dict():
    resource_id = str(uuid.uuid4())
    cloud_resource_id = str(uuid.uuid4())
    resource = r.Resource.from_dict(
        {
            "resource_id": resource_id,
            "cloud_resource_id": cloud_resource_id,
            "resource_name": "i-193b1a174798b8ede",
            "cloud_type": "aws",
        }
    )
    assert resource.resource_id == resource_id
    assert resource.cloud_resource_id == cloud_resource_id
    assert resource.resource_name == "i-193b1a174798b8ede"
    assert resource.cloud_type == "aws"
