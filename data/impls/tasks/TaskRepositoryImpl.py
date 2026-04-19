from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from data.helpers.exceptions import RepoException
from data.models.task_model import Task
from domain.repos.tasks.TaskRepository import TaskRepository

from data.helpers.db import AsyncSessionLocal

class TaskRepositoryImpl(TaskRepository):
    async def save_task_to_db(self, task: Task):
        async with AsyncSessionLocal() as db:
            try:
                db.add(task)
                await db.commit()
                await db.refresh(task)
                return task
            except IntegrityError as e:
                await db.rollback()
                raise RepoException(str(e))
            except Exception as e:
                await db.rollback()
                raise RepoException(str(e))

    async def get_task_from_db(self, user_id: str):
        async with AsyncSessionLocal() as db:
            try:
                result = await db.execute(
                    select(Task).where(Task.user_id == user_id)
                )
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise RepoException(str(e))

    async def update_task_to_db(self, task: Task):
        async with AsyncSessionLocal() as db:
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

    async def delete_task_simulation(self, task_id: str):
        async with AsyncSessionLocal() as db:
            try:
                dl_query = (
                    update(Task)
                    .where(Task.id == task_id)
                    .values(is_deleted=True)
                )
                await db.execute(dl_query)
                await db.commit()
            except Exception as e:
                await db.rollback()
                raise RepoException(str(e))