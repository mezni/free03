""" Module for repositories
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from src.domain.entities import Provider


class ProviderRepositoryInterface(ABC):
    """Interface ProviderRepositoryInterface"""

    @abstractmethod
    def create_provider(self, payload: Dict) -> Optional[Provider]:
        pass
