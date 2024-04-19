""" This module has definition of the Profession entity
"""

from dataclasses import dataclass, asdict
from src.domain.value_objects import Code


@dataclass
class Period:
    """Definition of the Period entity"""

    period_code: Code
    period_name: str

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(**data)

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)
