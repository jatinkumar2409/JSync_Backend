from datetime import datetime

from sqlalchemy import update, select, and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from data.helpers.exceptions import RepoException
from data.models.task_completion_model import TaskCompletion
from data.models.task_model import Task
from domain.repos.tasks.TaskCompletionRepo import TaskCompletionRepo

from data.helpers.db import AsyncSessionLocal  # 👈 import sessionmaker


class TaskCompletionRepoImpl(TaskCompletionRepo):
    async def save_task_completion(self, task_completion: TaskCompletion):
        async with AsyncSessionLocal() as db:
            try:
                db.add(task_completion)
                await db.commit()
                await db.refresh(task_completion)
                return task_completion
            except IntegrityError as e:
                await db.rollback()
                raise RepoException(str(e))
            except Exception as e:
                await db.rollback()
                raise RepoException(str(e))

    async def delete_task_completion(self, task_completion_id: str):
        async with AsyncSessionLocal() as db:
            try:
                dl_query = (
                    update(TaskCompletion)
                    .where(TaskCompletion.id == task_completion_id)
                    .values(is_deleted=True)
                )
                await db.execute(dl_query)
                await db.commit()
            except Exception as e:
                await db.rollback()
                raise RepoException(str(e))

    async def load_task_completion(self, start_of_day, end_of_day, user_id: str):
        async with AsyncSessionLocal() as db:
            try:
                start = datetime.fromtimestamp(start_of_day / 1000)
                end = datetime.fromtimestamp(end_of_day / 1000)
                result = await db.execute(
                    select(TaskCompletion)
                    .join(Task, TaskCompletion.task_id == Task.id)
                    .where(
                        and_(
                            Task.user_id == user_id,
                            TaskCompletion.completion_date >= start,
                            TaskCompletion.completion_date <= end,
                            TaskCompletion.is_deleted == False
                        )
                    )
                    .order_by(TaskCompletion.completion_date.desc())
                )
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise RepoException(str(e))