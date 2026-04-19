from pydantic import BaseModel
from fastapi import WebSocket

from data.schemas.task_completion_schema import TaskCompletionDto
from data.schemas.task_schema import TaskDTO


class AiRequestDTO(BaseModel):
    tasks : list[TaskDTO] = []
    message : str


