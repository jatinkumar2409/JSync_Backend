from typing import Optional

from pydantic import BaseModel

from data.schemas.task_completion_schema import TaskCompletionDto
from data.schemas.task_schema import TaskDTO


class WebsocketMessage(BaseModel):
    type : str
    task : Optional[TaskDTO] = None
    taskCompletion : Optional[TaskCompletionDto] = None
    error : Optional[str] = None