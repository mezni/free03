from abc import ABC, abstractmethod
from src.domain.provider import Provider


class ProviderRepository(ABC):
    @abstractmethod
    async def add_provider(self, provider_name: str) -> Provider:
        pass
