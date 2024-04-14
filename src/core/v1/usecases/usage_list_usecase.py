""" Module for Usage use cases"""


class UsageListUseCase:

    def __init__(self, repo):
        self.repo = repo

    def execute(self):
        return self.repo.list()
