""" Module for repositories
"""

from typing import Dict
from src.domain.entities import Provider
from src.interractor.repositories import ProviderRepositoryInterface


class InMemoryProviderRepository(ProviderRepositoryInterface):
    """Repository InMemoryProviderRepository"""

    def __init__(self):
        self._data: []

    def create_provider(self, payload: Dict) -> Provider:
        pass
