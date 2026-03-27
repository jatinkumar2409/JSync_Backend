from typing import Optional

from pydantic import BaseModel


class TaskDTO(BaseModel):
    id : str
    taskName : str
    userId : str
    dueAt : Optional[int]
    type : int
    priority : int
    hasDone : bool
    tags : str
    updatedAt : int = 0
