from data.helpers.exceptions import RepoException, UseCaseException
from data.helpers.jwt_auth import verify_token
from data.schemas.task_schema import TaskDTO
from domain.repos.tasks.TaskRepository import TaskRepository


class GetTasksUseCase:
    def __init__(self , repo : TaskRepository):
        self.repo = repo

    async def execute(self , token : str):
        try:
            user = verify_token(token=token , token_type="access")
            if not user:
                raise UseCaseException("User not found")
            tasks = await self.repo.get_task_from_db(user["id"])
            tasks_dto = [TaskDTO(id=task.id , taskName=task.task_name, userId=task.user_id , dueAt= int(task.due_at.timestamp() * 1000) if task.due_at else None , type=task.type , priority=task.priority ,
                                 hasDone=task.has_done , tags=task.tags , updatedAt= int(task.updated_at.timestamp()))   for task in tasks]
            return tasks_dto
        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
            raise UseCaseException(str(e))
