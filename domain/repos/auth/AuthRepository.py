from abc import ABC, abstractmethod
from data.models.user_model import User
class AuthRepository(ABC):
    @abstractmethod
    async def get_user_from_email(self , email : str):
        pass

    @abstractmethod
    async def save_user_to_db(self , user : User):
        pass

    @abstractmethod
    async def get_user_from_db(self , email : str , password : str):
        pass