import uuid
from src.domain.provider import Provider
from src.interactor.interfaces.provider_repository import ProviderRepository


class ProviderUseCase:
    def __init__(self, repo: ProviderRepository):
        self.repo = repo


    async def execute(self, provider_name: str) -> Provider:
        payload = {"provider_code": uuid.uuid4(), "provider_name": provider_name}
        return await self.repo.add_provider(payload)