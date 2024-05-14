class CreateUser:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, user):
        self.repo.create(user)
