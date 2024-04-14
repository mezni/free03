""" Module for Usage entity"""


class Usage:
    """Definition of the Usage entity"""

    def __init__(self, usage_id, org_id):
        self.usage_id = usage_id
        self.org_id = org_id

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(usage_id=data["usage_id"],org_id=data["org_id"])

    def to_dict(self):
        """Convert data into dictionary"""
        return {
            "usage_id": self.usage_id,"org_id": self.org_id,
        }
