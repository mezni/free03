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


class Resource:
    """Definition of the Resource entity"""

    def __init__(
        self,
        resource_code,
        resource_id,
        resource_name,
    ):
        self.resource_code = resource_code
        self.resource_id = resource_id
        self.resource_name = resource_name

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(
            resource_code=data["resource_code"],
            resource_id=data["resource_id"],
            resource_name=data["resource_name"],
        )

    def to_dict(self):
        """Convert data into dictionary"""
        return {
            "resource_code": self.resource_code,
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
        }


class Period:
    """Definition of the Period entity"""

    def __init__(
        self,
        period_code,
        period,
    ):
        self.period_code = period_code
        self.period = period

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(
            period_code=data["period_code"],
            period=data["period"],
        )

    def to_dict(self):
        """Convert data into dictionary"""
        return {
            "period_code": self.period_code,
            "period": self.period,
        }
