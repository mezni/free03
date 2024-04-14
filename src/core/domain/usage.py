""" Module for Usage entity"""


class Usage:
    """Definition of the Usage entity"""

    def __init__(
        self,
        usage_id,
        resource_id,
        period,
        usage_amount,
        usage_currency,
    ):
        self.usage_id = usage_id
        self.resource_id = resource_id
        self.period = period
        self.usage_amount = usage_amount
        self.usage_currency = usage_currency

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(
            usage_id=data["usage_id"],
            resource_id=data["resource_id"],
            period=data["period"],
            usage_amount=data["usage_amount"],
            usage_currency=data["usage_currency"],
        )

    def to_dict(self):
        """Convert data into dictionary"""
        return {
            "usage_id": self.usage_id,
            "resource_id": self.resource_id,
            "period": self.period,
            "usage_amount": self.usage_amount,
            "usage_currency": self.usage_currency,
        }

    def __eq__(self, other):
        """Compare two objects"""
        return self.to_dict() == other.to_dict()
