""" Module for CreateProfession Dtos
"""

from dataclasses import dataclass, asdict
from src.domain.value_objects import Code
from src.domain.entities.period import Period


@dataclass
class PeriodInputDto:
    """Input Dto for create Period"""

    period_code: Code
    period_name: str

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


@dataclass
class PeriodOutputDto:
    """Output Dto for create Period"""

    period: Period
