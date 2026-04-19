from datetime import datetime

from data.helpers.exceptions import UseCaseException, RepoException
from data.models.task_model import Task
from data.schemas.task_schema import TaskDTO
from domain.repos.tasks.TaskRepository import TaskRepository


class UpdateTaskUseCase:
    def __init__(self , repo : TaskRepository):
        self.repo = repo

    async def execute(self , task_dto : TaskDTO):
        try:
            due_at = None
            if task_dto.dueAt is not None:
                due_at = datetime.fromtimestamp(task_dto.dueAt / 1000)
            task = Task(
                id=task_dto.id, task_name=task_dto.taskName, user_id=task_dto.userId, due_at=due_at,
                type=task_dto.type, priority=task_dto.priority, has_done=task_dto.hasDone, tags=task_dto.tags  , belongs_to_date = datetime.fromtimestamp(task_dto.belongsToDate / 1000) ,
                expiry_time= datetime.fromtimestamp(task_dto.expiryTime / 1000) if task_dto.expiryTime is not None else None
            )
            await self.repo.update_task_to_db(task)
        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
            raise UseCaseException(str(e))