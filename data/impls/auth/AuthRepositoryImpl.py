from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from data.helpers.exceptions import RepoException
from data.models.user_model import User

from data.helpers.db import AsyncSessionLocal
from domain.repos.auth.AuthRepository import AuthRepository


class AuthRepositoryImpl(AuthRepository):

    async def get_user_from_email(self, email: str):
        async with AsyncSessionLocal() as db:
            try:
                result = await db.execute(
                    select(User).where(User.email == email)
                )
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                raise RepoException(str(e))

    async def save_user_to_db(self, user: User):
        async with AsyncSessionLocal() as db:
            try:
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return user
            except IntegrityError as e:
                await db.rollback()
                raise RepoException(str(e))
            except SQLAlchemyError as e:
                await db.rollback()
                raise RepoException(str(e))

    async def get_user_from_db(self, email: str, password: str):
        async with AsyncSessionLocal() as db:
            try:
                result = await db.execute(
                    select(User).where(
                        and_(
                            User.email == email,
                            User.password == password
                        )
                    )
                )
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                raise RepoException(str(e))