from abc import ABC, abstractmethod

from data.models.user_model import User


class TokenRepository(ABC):
    @abstractmethod
    async def save_session(self , user : dict):
        pass

    @abstractmethod
    async def delete_session(self , user_id : str):
        pass



