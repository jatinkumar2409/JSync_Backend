from data.helpers.exceptions import UseCaseException, RepoException
from domain.repos.tasks.TaskCompletionRepo import TaskCompletionRepo



class LoadTaskCompletions:
    def __init__(self , repo : TaskCompletionRepo):
        self.repo = repo

    async def execute(self , start_of_day, end_of_day , user_id):
        repo = self.repo
        try:
           task_completions = await repo.load_task_completion(start_of_day, end_of_day , user_id)
           return task_completions
        except RepoException as e:
            raise UseCaseException(str(e))
        except Exception as e:
            raise UseCaseException(str(e))