from data.helpers.exceptions import UseCaseException
from domain.repos.tasks.TaskCompletionRepo import TaskCompletionRepo


class DeleteTaskCompletionUseCase:
    def __init__(self , repo : TaskCompletionRepo):
        self.repo = repo

    async def execute(self , task_completion_id : str):
        try:
            await self.repo.delete_task_completion(task_completion_id)
        except Exception as e:
            raise UseCaseException(str(e))