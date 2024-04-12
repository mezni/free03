class Resource:
    def __init__(self, resource_id, cloud_resource_id, resource_name, cloud_type):
        self.resource_id = resource_id
        self.cloud_resource_id = cloud_resource_id
        self.resource_name = resource_name
        self.cloud_type = cloud_type

    @classmethod
    def from_dict(cls, adict):
        return cls(
            resource_id=adict["resource_id"],
            cloud_resource_id=adict["cloud_resource_id"],
            resource_name=adict["resource_name"],
            cloud_type=adict["cloud_type"],
        )

    def to_dict(self):
        return {
            "resource_id": self.resource_id,
            "cloud_resource_id": self.cloud_resource_id,
            "resource_name": self.resource_name,
            "cloud_type": self.cloud_type,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
