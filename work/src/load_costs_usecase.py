class LoadCostsUseCase:
    def __init__(self, repo):
        self.repo = repo

    def process(self, data_source: str, data_path: str):
        print(data_source, data_path)
        return None
