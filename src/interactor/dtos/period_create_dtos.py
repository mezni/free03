""" Module for CreatePeriod Dtos
"""

from dataclasses import dataclass, asdict
from src.domain.entities.period import Period


@dataclass
class CreatePeriodInputDto:
    """Input Dto for create Period"""

    period_name: str

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


@dataclass
class CreatePeriodOutputDto:
    """Output Dto for create Period"""

    period: Period
