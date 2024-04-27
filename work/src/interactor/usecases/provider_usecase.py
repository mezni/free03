from src.interactor.repository.provider_repository import ProviderRepositoryInterface


class ProviderCreateUsecase:
    def __init__(self, repo):
        self.repo = repo

    async def create(self, provider_name: str):
        await self.repo.create_provider(provider_name)
