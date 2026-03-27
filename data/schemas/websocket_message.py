from typing import Optional

from pydantic import BaseModel

from data.schemas.task_schema import TaskDTO


class WebsocketMessage(BaseModel):
    type : str
    task : Optional[TaskDTO]
    error : Optional[str]