from data.helpers.exceptions import RepoException, UseCaseException
from data.helpers.jwt_auth import verify_token
from data.schemas.task_schema import TaskDTO
from domain.repos.tasks.TaskRepository import TaskRepository


class GetTasksUseCase:
    def __init__(self , repo : TaskRepository):
        self.repo = repo

    async def execute(self , user_id : str):
        try:
            tasks = await self.repo.get_task_from_db(user_id)
            for task in tasks:
                print(task.id, task.belongs_to_date)
            tasks_dto = [TaskDTO(id=task.id , taskName=task.task_name, userId=task.user_id , dueAt= int(task.due_at.timestamp() * 1000) if task.due_at else None , type=task.type , priority=task.priority ,
                                 hasDone=task.has_done , tags=task.tags , updatedAt= int(task.updated_at.timestamp()) , isDeleted=task.is_deleted , expiryTime=int(task.expiry_time.timestamp() * 1000) if task.expiry_time is not None else None , belongsToDate=int(task.belongs_to_date.timestamp() * 1000))   for task in tasks]
            return tasks_dto
        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
            raise UseCaseException(str(e))
