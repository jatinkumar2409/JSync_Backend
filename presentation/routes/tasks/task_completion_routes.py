from fastapi import APIRouter, Request, HTTPException, Depends

from data.helpers.exceptions import UseCaseException, TokenExpiredException
from data.helpers.jwt_auth import verify_token
from data.schemas.task_completion_schema import TaskCompletionDto
from domain.usecases.tasks.task_completions.AddTaskCompletionUseCase import AddTaskCompletionUseCase
from domain.usecases.tasks.task_completions.DeleteTaskCompletionUseCase import DeleteTaskCompletionUseCase
from domain.usecases.tasks.task_completions.LoadTaskCompletionsUseCase import LoadTaskCompletions
from presentation.deps.dependencies import add_task_completion_use_case, delete_task_completion_use_case, \
    get_task_completions_use_case

task_completion_router = APIRouter()

@task_completion_router.post("/add_task_completion")
async def add_task_completion(request : Request , task_completion_dto : TaskCompletionDto , usecase : AddTaskCompletionUseCase = Depends(add_task_completion_use_case)):
    try:
        token = request.headers.get("Authorization")
        payload = verify_token(token_with_scheme=token, token_type="access")
        await usecase.execute(task_completion_dto)
    except TokenExpiredException as e:
        raise HTTPException(status_code=401 , detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

@task_completion_router.delete("/delete_task_completion")
async def delete_task_completion(request : Request , id : str , usecase : DeleteTaskCompletionUseCase = Depends(delete_task_completion_use_case)):
    try:
        token = request.headers.get("Authorization")
        payload = verify_token(token_with_scheme=token, token_type="access")
        await usecase.execute(id)
    except TokenExpiredException as e:
        raise HTTPException(status_code=401 , detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

@task_completion_router.get("/load_task_completions")
async def load_task_completions(request : Request , start_of_day : int , end_of_day : int , usecase : LoadTaskCompletions = Depends(get_task_completions_use_case)):
    try:
        print("load tasks completions is being called")
        token = request.headers.get("Authorization")
        payload = verify_token(token_with_scheme=token, token_type="access")
        user_id = payload["id"]
        task_completions = await usecase.execute(start_of_day=start_of_day , end_of_day=end_of_day , user_id=user_id)
        return task_completions
    except TokenExpiredException as e:
        print(f"Exception at load task completion is {str(e)}")
        raise HTTPException(status_code=401 , detail=str(e))
    except Exception as e:
        print(f"Exception at load task completion is {str(e)}")
        raise HTTPException(status_code=500 , detail=str(e))