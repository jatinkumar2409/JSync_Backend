from pydantic import BaseModel


class TaskCompletionDto(BaseModel):
    id : str
    taskId : str
    completionDate : int
    isDeleted : bool = False