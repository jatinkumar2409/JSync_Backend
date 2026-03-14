from sqlalchemy import delete

from data.helpers.exceptions import RepoException
from data.helpers.jwt_auth import create_refresh_token
from data.models.session_model import Session
from data.models.user_model import User
from domain.repos.auth.TokenRepository import TokenRepository
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
class TokenRepositoryImpl(TokenRepository):
    def __init__(self , db):
        self.db = db
    async def save_session(self , user : dict):
        try:
            token = create_refresh_token(user)
            session = Session(id = token , user_id = user["id"])
            self.db.add(session)
            await self.db.commit()
            await self.db.refresh(session)
            return session
        except IntegrityError as e:
            await self.db.rollback()
            raise RepoException(str(e))
        except SQLAlchemyError as e:
            print(e)
            await self.db.rollback()
            raise RepoException(str(e))

    async def delete_session(self , user_id : str):
        try:
           _del = delete(Session).where(Session.user_id == user_id)
           await self.db.execute(_del)
           await self.db.commit()
        except SQLAlchemyError as e:
            print(e)
            await self.db.rollback()
            raise RepoException(str(e))
