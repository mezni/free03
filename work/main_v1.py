import asyncio


class PeriodRepository:
    pass


class RepoRegistry:
    def __init__(self):
        self.repositories = {}

    def register_repository(self, name, repository):
        self.repositories[name] = repository

    def get_repository(self, name):
        return self.repositories.get(name)


class LoadUsageUseCase:
    def __init__(self, repos):
        self.repos = repos

    def process(self, usage_data):
        pass


async def main():
    print("# Enter")
    usage_date = ["2024-04-25"]
    repos = RepoRegistry()
    repos.register_repository("period_repo", PeriodRepository())

    load_usage_usecase = LoadUsageUseCase(repos)
    load_usage_usecase.process(usage_date)


#    load_usage_usecase.repos.get_repository(period_repo)


asyncio.run(main())
