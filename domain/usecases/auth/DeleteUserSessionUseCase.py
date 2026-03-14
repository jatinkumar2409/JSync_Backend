from data.helpers.exceptions import UseCaseException, RepoException
from domain.repos.auth.TokenRepository import TokenRepository

class DeleteUserSessionUseCase:
    def __init__(self , token_repo : TokenRepository):
        self.token_repo = token_repo

    async def execute(self , user_id : str):
        try:
          await self.token_repo.delete_session(user_id)

        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
           raise UseCaseException(str(e))
