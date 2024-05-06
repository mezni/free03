from src.domain.provider import Provider
from src.interactor.interfaces.provider_repository import ProviderRepository


class AddProviderUseCase:
    def __init__(self, repo: ProviderRepository):
        self.repo = repo

    async def execute(self, provider_name: str) -> Provider:
        return await self.repo.add_provider(provider_name)
