from typing import Dict, List
from abc import ABC, abstractmethod
from src.domain.provider import Provider


class ProviderRepository(ABC):
    @abstractmethod
    async def add_provider(self, payload: Dict) -> Provider:
        pass

    @abstractmethod
    async def get_provider_by_name(self, provider_name: str) -> Provider:
        pass

    @abstractmethod
    async def get_providers(self) -> List[Provider]:
        pass
