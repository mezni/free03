from src.core.v1.domain import usage as u


class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self):
        return [u.Usage.from_dict(i) for i in self.data]