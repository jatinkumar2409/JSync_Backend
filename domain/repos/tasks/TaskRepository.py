from abc import abstractmethod , ABC
from data.models.task_model import Task
class TaskRepository(ABC):
    @abstractmethod
    async def save_task_to_db(self , task):
        pass

    @abstractmethod
    async def get_task_from_db(self , user_id : str):
        pass

    @abstractmethod
    async def update_task_to_db(self , task):
        pass

    @abstractmethod
    async def delete_task_simulation(self , task_id : str):
        pass