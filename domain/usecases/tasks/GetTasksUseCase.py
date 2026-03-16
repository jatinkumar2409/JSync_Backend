from data.helpers.exceptions import RepoException, UseCaseException
from domain.repos.tasks.TaskRepository import TaskRepository


class GetTasksUseCase:
    def __init__(self , repo : TaskRepository):
        self.repo = repo

    async def execute(self , user_id : str):
        try:
            tasks = await self.repo.get_task_from_db(user_id)
            return tasks
        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
            raise UseCaseException(str(e))
