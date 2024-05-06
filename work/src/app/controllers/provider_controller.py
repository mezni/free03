from src.domain.provider import Provider
from src.interactor.usecases.provider_usecase import AddProviderUseCase


class ProviderController:
    def __init__(self, usecase: AddProviderUseCase):
        self.usecase = usecase

    async def add_provider(self, provider_name: str) -> Provider:
        return await self.usecase.execute(provider_name)
