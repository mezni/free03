from typing import Dict, List
from src.domain.provider import Provider
from src.interactor.interfaces.provider_repository import ProviderRepository


class AddProviderUseCase:
    def __init__(self, repo: ProviderRepository):
        self.repo = repo

    async def execute(self, provider_name: str) -> Provider:
        payload = {"provider_code": "Ford", "provider_name": provider_name}  # DTO
        return await self.repo.add_provider(payload)


class GetProviderByNameUseCase:
    def __init__(self, repo: ProviderRepository):
        self.repo = repo

    async def execute(self, provider_name: str) -> Provider:
        return await self.repo.get_provider_by_name(provider_name)


class GetProvidersUseCase:
    def __init__(self, repo: ProviderRepository):
        self.repo = repo

    async def execute(self) -> List[Provider]:
        return await self.repo.get_providers()
