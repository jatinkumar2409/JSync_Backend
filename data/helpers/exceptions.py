class RepoException(Exception):
    def __init__(self , message : str = "Repo Exception"):
        self.message = message
        super().__init__(self.message)

class UseCaseException(Exception):
    def __init__(self , message : str = "UseCase Exception"):
        self.message = message
        super().__init__(self.message)


class WebsocketException(Exception):
    def __init__(self , message : str = "Websocket Exception"):
        self.message = message
        super().__init__(self.message)


class TokenExpiredException(Exception):
    def __init__(self , message : str = "Token Expired"):
        self.message = message
        super().__init__(self.message)

class TokenValidationException(Exception):
    def __init__(self , message : str = "Token Expired"):
        self.message = message
        super().__init__(self.message)