import json
import uuid

from costs.serializers import resource_json_serializer as ser
from costs.domain import resource as r


def test_serialize_domain_resource():
    resource_id = str(uuid.uuid4())
    cloud_resource_id = str(uuid.uuid4())
    resource_dict = {
        "resource_id": resource_id,
        "cloud_resource_id": cloud_resource_id,
        "resource_name": "i-193b1a174798b8ede",
        "cloud_type": "aws",
    }
    resource = r.Resource.from_dict(resource_dict)

    expected_json = """
        {{
            "resource_id": "{}",
            "cloud_resource_id": "{}",
            "resource_name": "i-193b1a174798b8ede",
            "cloud_type": "aws"
        }}
    """.format(
        resource_id, cloud_resource_id
    )

    json_resource = json.dumps(resource, cls=ser.ResourceJsonEncoder)

    assert json.loads(json_resource) == json.loads(expected_json)
