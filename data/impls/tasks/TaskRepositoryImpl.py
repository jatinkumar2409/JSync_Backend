from fastapi import HTTPException
from sqlalchemy import select, update, delete

from data.helpers.exceptions import RepoException
from data.models.task_model import Task
from domain.repos.tasks.TaskRepository import TaskRepository
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


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

    async def get_task_from_db(self , user_id : str):
        db = self.db
        try:
            result = await db.execute(
                select(Task).where(
                    Task.user_id == user_id
                )
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RepoException(str(e))

    async def update_task_to_db(self , task):
        db = self.db
        try:
            task_query = (
                update(Task)
                .where(Task.id == task.id)
                .values(
                    task_name=task.task_name,
                    user_id=task.user_id,
                    due_at=task.due_at,
                    type=task.type,
                    priority=task.priority,
                    has_done=task.has_done,
                    tags=task.tags,
                    is_deleted=task.is_deleted,
                )
            )
            await db.execute(task_query)
            await db.commit()

        except Exception as e:
            await db.rollback()
            raise RepoException(str(e))

    async def delete_task_from_db(self , task_id):
        db = self.db
        try:
            dl_query = delete(Task).where(Task.id == task_id)
            await db.execute(dl_query)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise RepoException(str(e))
