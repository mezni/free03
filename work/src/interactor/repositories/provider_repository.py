from typing import Dict
from abc import ABC, abstractmethod


class ProviderRepositoryInterface(ABC):
    @abstractmethod
    async def create_provider(self, payload: Dict):
        pass

    @abstractmethod
    async def get_provider_by_name(self, provider_name: str):
        pass

    @abstractmethod
    async def get_all_provider(self):
        pass
