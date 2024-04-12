import json


class ResourceJsonEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            to_serialize = {
                "resource_id": o.resource_id,
                "cloud_resource_id": o.cloud_resource_id,
                "resource_name": o.resource_name,
                "cloud_type": o.cloud_type,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
