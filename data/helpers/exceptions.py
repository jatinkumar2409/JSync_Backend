class RepoException(Exception):
    def __init__(self , message : str = "Repo Exception"):
        self.message = message
        super().__init__(self.message)

class UseCaseException(Exception):
    def __init__(self , message : str = "UseCase Exception"):
        self.message = message
        super().__init__(self.message)
