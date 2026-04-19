import uuid

from sqlalchemy import delete

from data.helpers.exceptions import RepoException
from data.helpers.jwt_auth import create_refresh_token
from data.models.session_model import Session
from data.models.user_model import User
from domain.repos.auth.TokenRepository import TokenRepository
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from data.helpers.db import AsyncSessionLocal
class TokenRepositoryImpl(TokenRepository):

    async def save_session(self , user : dict):
      async with AsyncSessionLocal() as db:
        try:
            user["duc"] = str(uuid.uuid4())
            token = create_refresh_token(user)
            session = Session(id = token , user_id = user["id"])
            db.add(session)
            await db.commit()
            await db.refresh(session)
            return session
        except IntegrityError as e:
            print(e)
            await db.rollback()
            raise RepoException(str(e))
        except SQLAlchemyError as e:
            print(e)
            await db.rollback()
            raise RepoException(str(e))

    async def delete_session(self , user_id : str):
      async with AsyncSessionLocal() as db:
        try:
           _del = delete(Session).where(Session.user_id == user_id)
           await db.execute(_del)
           await db.commit()
        except SQLAlchemyError as e:
            print(e)
            await db.rollback()
            raise RepoException(str(e))
