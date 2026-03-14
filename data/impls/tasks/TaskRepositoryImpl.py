from fastapi import HTTPException

from data.helpers.exceptions import RepoException
from data.models.task_model import Task
from domain.repos.tasks.TaskRepository import TaskRepository
from sqlalchemy.exc import IntegrityError

class TaskRepositoryImpl(TaskRepository):
    def __init__(self , db):
        self.db = db

    async def save_task_to_db(self , task : Task):
        db = self.db
        try:
            db.add(task)
            await db.commit()
            await db.refresh(task)
            print(task)
        except IntegrityError as e:
            print(e)
            raise RepoException(str(e))
        except Exception as e:
            print(e)
            raise RepoException(str(e))

