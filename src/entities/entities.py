""" Module for entities """


class Usage:
    """Definition of the Usage entity"""

    def __init__(
        self,
        usage_code,
        resource_code,
        usage_amount,
        usage_currency,
    ):
        self.usage_code = usage_code
        self.resource_code = resource_code
        self.usage_amount = usage_amount
        self.usage_currency = usage_currency

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(
            usage_code=data["usage_code"],
            resource_code=data["resource_code"],
            usage_amount=data["usage_amount"],
            usage_currency=data["usage_currency"],
        )

    def to_dict(self):
        """Convert data into dictionary"""
        return {
            "usage_code": self.usage_code,
            "resource_code": self.resource_code,
            "usage_amount": self.usage_amount,
            "usage_currency": self.usage_currency,
        }
