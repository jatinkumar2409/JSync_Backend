from fastapi import APIRouter, HTTPException, Depends , WebSocket , Request
from starlette.websockets import WebSocketDisconnect

from data.helpers.exceptions import UseCaseException, WebsocketException
from data.helpers.jwt_auth import verify_token
from data.impls.tasks.ConnectionRepoImpl import ConnectionRepoImpl
from data.schemas.task_schema import TaskDTO
from domain.repos.tasks.ConnectionRepository import ConnectionRepository
from domain.repos.tasks.TaskRepository import TaskRepository
from domain.usecases.tasks.AddTaskUseCase import AddTaskUseCase
from domain.usecases.tasks.DeleteTaskUseCase import DeleteTaskUseCase
from domain.usecases.tasks.GetTasksUseCase import GetTasksUseCase
from domain.usecases.tasks.UpdateTaskUseCase import UpdateTaskUseCase
from presentation.deps.dependencies import add_task_use_case, get_tasks_use_case, get_task_repo, \
    get_task_connection_repo, update_task_use_case, delete_task_use_case

task_router = APIRouter()

@task_router.post("/add_task")
async def add_task(request : Request , task_dto : TaskDTO , usecase : AddTaskUseCase = Depends(add_task_use_case)):
   try:
       token = request.headers.get("Authorization")
       payload = verify_token(token=token , token_type="access")
       await usecase.execute(task_dto)
       return {"success" : True}
   except UseCaseException as e:
       raise HTTPException(status_code=500 , detail= str(e))
   except Exception as e:
       raise HTTPException(status_code=500 , detail=str(e))


@task_router.get("/get_tasks")
async def get_tasks(request : Request, usecase : GetTasksUseCase = Depends(get_tasks_use_case)):
    try:
        for key, value in request.headers.items():
            print(f"{key}: {value}")
        token = request.headers.get("Authorization")
        print(f"Access token is {token}")
        tasks = await usecase.execute(token)
        return tasks
    except UseCaseException as e:
        raise HTTPException(status_code=500 , detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

@task_router.put("/update_task")
async def update_task(request : Request  , task_dto : TaskDTO, usecase : UpdateTaskUseCase = Depends(update_task_use_case)):
    try:
        token = request.headers.get("Authorization")
        payload = verify_token(token = token , token_type = "access")
        await usecase.execute(task_dto)
        return {"success" : True}
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

@task_router.delete("/delete_task")
async def delete_task(request : Request , task_id : str , usecase : DeleteTaskUseCase = Depends(delete_task_use_case)):
    try:
        token = request.headers.get("Authorization")
        payload = verify_token(token=token , token_type="access")
        await usecase.execute(task_id)
        return {"success" : True}
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

@task_router.websocket("/ws/tasks")
async def manage_tasks_websocket(websocket : WebSocket , repo : ConnectionRepository = Depends(get_task_connection_repo) , add_task : AddTaskUseCase = Depends(add_task_use_case)):
    try:
        user_id = await repo.validate_connection(websocket)
        if not user_id:
            return
        await websocket.accept()
        await repo.connect(user_id=user_id, websocket=websocket)
        while True:
                data = await websocket.receive_json()
                print(data)
                await repo.send_message(user_id=user_id  , websocket=websocket, message=data , add_task_use_case=add_task)

    except WebSocketDisconnect:
           await repo.disconnect(user_id=user_id , websocket=websocket)

    except Exception as e:
        print(e)
        await repo.disconnect(user_id=user_id, websocket=websocket)
        await websocket.close(code=1011)




