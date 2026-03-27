from fastapi import HTTPException

from data.helpers.exceptions import RepoException, UseCaseException
from data.helpers.jwt_auth import create_access_token
from data.models.session_model import Session
from data.schemas.user_schema import User_Schema
from domain.repos.auth.AuthRepository import AuthRepository
from domain.repos.auth.TokenRepository import TokenRepository

class LogUserInUseCase:
    def __init__(self , auth_repo : AuthRepository , token_repo : TokenRepository):
        self.repo = auth_repo
        self.token_repo = token_repo

    async def execute(self , email : str , password :str):
        try:
            user = await self.repo.get_user_from_db(email , password)
            if user is None:
                raise UseCaseException()
            user_dict = User_Schema(
                id=user.id,
                name=user.name,
                password=user.password,
                email=user.email,
                profile=user.profile
            )
            session: Session = await self.token_repo.save_session(user_dict.dict())
            access_token = create_access_token(user_dict.dict())
            return [access_token , session.id , user.id]
        except RepoException as e:
            print(e)
            raise UseCaseException(str(e))
        except Exception as e:
            print(e)
            raise UseCaseException(str(e))
