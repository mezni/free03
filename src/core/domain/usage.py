""" Module for Usage entity"""


class Usage:
    """Definition of the Usage entity"""

    def __init__(
        self,
        usage_id,
        org_id,
        source_id,
        provider,
        resource_id,
        resource_name,
        period,
        usage_amount,
        usage_currency,
    ):
        self.usage_id = usage_id
        self.org_id = org_id
        self.source_id = source_id
        self.provider = provider
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.period = period
        self.usage_amount = usage_amount
        self.usage_currency = usage_currency

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(
            usage_id=data["usage_id"],
            org_id=data["org_id"],
            source_id=data["source_id"],
            provider=data["provider"],
            resource_id=data["resource_id"],
            resource_name=data["resource_name"],
            period=data["period"],
            usage_amount=data["usage_amount"],
            usage_currency=data["usage_currency"],
        )

    def to_dict(self):
        """Convert data into dictionary"""
        return {
            "usage_id": self.usage_id,
            "org_id": self.org_id,
            "source_id": self.source_id,
            "provider": self.provider,
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "period": self.period,
            "usage_amount": self.usage_amount,
            "usage_currency": self.usage_currency,
        }
