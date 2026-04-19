from abc import ABC , abstractmethod

class TaskCompletionRepo(ABC):

    @abstractmethod
    async def save_task_completion(self , task_completion):
        pass

    @abstractmethod
    async def delete_task_completion(self , task_completion_id):
        pass

    @abstractmethod
    async def load_task_completion(self , start_of_day, end_of_day , user_id):
        pass