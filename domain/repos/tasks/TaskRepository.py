from abc import abstractmethod , ABC
from data.models.task_model import Task
class TaskRepository(ABC):
    @abstractmethod
    async def save_task_to_db(self , task : Task):
        pass

    @abstractmethod
    async def get_task_from_db(self , user_id : str):
        pass