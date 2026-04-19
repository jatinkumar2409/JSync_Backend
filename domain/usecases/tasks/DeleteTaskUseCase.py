from data.helpers.exceptions import UseCaseException, RepoException
from domain.repos.tasks.TaskRepository import TaskRepository


class DeleteTaskUseCase:
    def __init__(self , repo : TaskRepository):
        self.repo = repo

    async def execute(self ,task_id : str):
        try:
            await self.repo.delete_task_simulation(task_id)
        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
            raise UseCaseException(str(e))
