from abc import abstractmethod , ABC
from data.models.task_model import Task
class TaskRepository(ABC):
    @abstractmethod
    async def save_task_to_db(self , task : Task):
        pass