from src.interractor.interfaces import LoggerInterface


class CreateProviderController:
    def __init__(self, logger: LoggerInterface):
        self.logger = logger

    async def execute(self, data):
        pass


#        repository = ProviderInMemoryRepository()
