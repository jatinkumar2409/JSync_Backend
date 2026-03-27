from abc import ABC , abstractmethod

class ConnectionRepository(ABC):

    @abstractmethod
    async def validate_connection(self , websocket):
        pass

    @abstractmethod
    async def connect(self , user_id , websocket):
       pass

    @abstractmethod
    async def disconnect(self , user_id , websocket):
        pass

    @abstractmethod
    async def send_message(self  , websocket, user_id, message , add_task_use_case , update_task_use_case , delete_task_use_case):
        pass