from data.helpers.exceptions import RepoException, UseCaseException
from data.helpers.jwt_auth import create_access_token
from data.models.session_model import Session
from data.models.user_model import User
from data.schemas.user_schema import User_Schema
from domain.repos.auth.AuthRepository import AuthRepository
from domain.repos.auth.TokenRepository import TokenRepository


class RegisterUserUseCase:
    def __init__(self, auth_repo : AuthRepository , token_repo : TokenRepository):
        self.repo = auth_repo
        self.token_repo = token_repo

    async def execute(self , user : User):
        try:
            existing_user = await self.repo.get_user_from_email(user.email)
            if existing_user:
                raise ValueError("Email already exists")
            user = await self.repo.save_user_to_db(user)
            user_dict = User_Schema(
                id=user.id,
                name=user.name,
                password=user.password,
                email=user.email,
                profile=user.profile
            )
            session : Session = await self.token_repo.save_session(user_dict.dict())
            access_token = create_access_token(user_dict.dict())

            return [access_token , session.id , user.id]
        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
            raise UseCaseException(str(e))
