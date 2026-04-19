from data.models.task_completion_model import TaskCompletion
from data.schemas.task_completion_schema import TaskCompletionDto
from data.schemas.task_schema import TaskDTO
from data.schemas.websocket_message import WebsocketMessage
from domain.repos.tasks.ConnectionRepository import ConnectionRepository
from collections import defaultdict

from fastapi import WebSocket, Depends
from data.helpers.jwt_auth import verify_token
from domain.usecases.tasks.AddTaskUseCase import AddTaskUseCase
from domain.usecases.tasks.DeleteTaskUseCase import DeleteTaskUseCase
from domain.usecases.tasks.UpdateTaskUseCase import UpdateTaskUseCase
from domain.usecases.tasks.task_completions.AddTaskCompletionUseCase import AddTaskCompletionUseCase
from domain.usecases.tasks.task_completions.DeleteTaskCompletionUseCase import DeleteTaskCompletionUseCase


class ConnectionRepoImpl(ConnectionRepository):
    def __init__(self):
        self.connections = defaultdict(list)

    async def validate_connection(self , websocket : WebSocket):
       token = websocket.query_params.get("token")
       if not token:
           await websocket.close(code = 1008)
           return None
       user = verify_token(token_with_scheme= f"Bearer {token}", token_type="access")
       return user["id"]

    async def connect(self , user_id , websocket):
        self.connections[user_id].append(websocket)
        print("Websocket connected with" + user_id)


    async def disconnect(self , user_id , websocket):
        print("disconnect has been called")
        if user_id in self.connections:
            if websocket in self.connections[user_id]:
                self.connections[user_id].remove(websocket)
            if len(self.connections[user_id]) == 0:
                del self.connections[user_id]

    async def send_message(self , websocket, user_id , message , add_task_use_case : AddTaskUseCase ,
                           update_task_use_case : UpdateTaskUseCase , delete_task_use_case : DeleteTaskUseCase , add_task_completion_use_case : AddTaskCompletionUseCase , delete_task_completion_use_case : DeleteTaskCompletionUseCase):
        type = message["type"]
        try:
          if type == "ping":
                print("type is ping")
                await websocket.send_json(
                    WebsocketMessage(type="pong", task=None, taskCompletion=None, error=None).model_dump())
          else:
            task = message.get("task")
            task_completion = message.get("taskCompletion")
            if task and not task["userId"]:
              task["userId"] = user_id
            if type == "task":
              await add_task_use_case.execute(TaskDTO(**task))
            elif type == "update_task":
                await update_task_use_case.execute(TaskDTO(**task))
            elif type == "delete_task":
                await delete_task_use_case.execute(task["id"])
            elif type == "task_completion":
                await add_task_completion_use_case.execute(TaskCompletionDto(**task_completion))
            elif type == "delete_task_completion":
                await delete_task_completion_use_case.execute(task_completion["id"])

            for connection in self.connections[user_id]:
                print(f"Sending task {task}")
                await connection.send_json(WebsocketMessage(type=type, task=task , taskCompletion=task_completion, error=None).model_dump())
        except Exception as e:
            print("Exception : " +  str(e))
            await websocket.send_json(WebsocketMessage(type=f"error_for_{type}" , task= message.get("task") , taskCompletion=message.get("taskCompletion") , error=str(e)).model_dump())
connection_repo_impl = ConnectionRepoImpl()


