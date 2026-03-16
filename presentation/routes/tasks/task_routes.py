from fastapi import APIRouter, HTTPException, Depends
from data.helpers.exceptions import UseCaseException
from data.schemas.task_schema import TaskDTO
from domain.usecases.tasks.AddTaskUseCase import AddTaskUseCase
from domain.usecases.tasks.GetTasksUseCase import GetTasksUseCase
from presentation.deps.dependencies import add_task_use_case, get_tasks_use_case

task_router = APIRouter()

@task_router.post("/add_task")
async def add_task(task_dto : TaskDTO , usecase : AddTaskUseCase = Depends(add_task_use_case)):
   try:
       await usecase.execute(task_dto)
       return {"success" : True}
   except UseCaseException as e:
       raise HTTPException(status_code=500 , detail= str(e))
   except Exception as e:
       raise HTTPException(status_code=500 , detail=str(e))


@task_router.get("/get_tasks")
async def get_tasks(user_id : str , usecase : GetTasksUseCase = Depends(get_tasks_use_case)):
    try:
        return usecase.execute(user_id)
    except UseCaseException as e:
        raise HTTPException(status_code=500 , detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

