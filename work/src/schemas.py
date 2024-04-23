from dataclasses import dataclass, asdict
from src.entities import Period


@dataclass
class CreatePeriodIn:
    period_name: str

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


@dataclass
class CreatePeriodOut:
    """Output Dto for create profession"""

    period: Period
