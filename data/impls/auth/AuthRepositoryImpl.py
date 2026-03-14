from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

from data.helpers.exceptions import RepoException
from domain.repos.auth.AuthRepository import AuthRepository
from sqlalchemy.future import select
from data.models.user_model import User
class AuthRepositoryImpl(AuthRepository):
    def __init__(self , db):
        self.db = db

    async def get_user_from_email(self , email : str):
      try:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
      except SQLAlchemyError as e:
         print(e)
         raise RepoException(str(e))

    async def save_user_to_db(self ,user : User):
        self.db.add(user)
        try:
          await self.db.commit()
          await self.db.refresh(user)
          return user
        except IntegrityError as e:
            await self.db.rollback()
            raise RepoException(str(e))
        except SQLAlchemyError as e:
            print(e)
            await self.db.rollback()
            raise RepoException(str(e))


    async def get_user_from_db(self , email : str , password : str):
        try:
            result = await self.db.execute(
                select(User).where(
                    and_(User.email == email , User.password == password)
                )
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            print(e)
            raise RepoException(str(e))


