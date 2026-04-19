from datetime import datetime

from data.helpers.exceptions import UseCaseException
from data.models.task_completion_model import TaskCompletion
from data.schemas.task_completion_schema import TaskCompletionDto
from data.schemas.task_schema import TaskDTO
from domain.repos.tasks.TaskCompletionRepo import TaskCompletionRepo


class AddTaskCompletionUseCase:
    def __init__(self , task_completion_repo : TaskCompletionRepo):
        self.repo = task_completion_repo

    async def execute(self , task_completion_dto : TaskCompletionDto):
        try:
            task_completion = TaskCompletion(
                id = task_completion_dto.id , task_id = task_completion_dto.taskId , completion_date = datetime.fromtimestamp(task_completion_dto.completionDate / 1000)
            )
            await self.repo.save_task_completion(task_completion)
        except Exception as e:
            raise UseCaseException(str(e))