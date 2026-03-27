from data.schemas.task_schema import TaskDTO
from data.schemas.websocket_message import WebsocketMessage
from domain.repos.tasks.ConnectionRepository import ConnectionRepository
from collections import defaultdict

from fastapi import WebSocket, Depends
from data.helpers.jwt_auth import verify_token
from domain.usecases.tasks.AddTaskUseCase import AddTaskUseCase
from domain.usecases.tasks.DeleteTaskUseCase import DeleteTaskUseCase
from domain.usecases.tasks.UpdateTaskUseCase import UpdateTaskUseCase


class ConnectionRepoImpl(ConnectionRepository):
    def __init__(self):
        self.connections = defaultdict(list)

    async def validate_connection(self , websocket : WebSocket):
       token = websocket.query_params.get("token")
       if not token:
           await websocket.close(code = 1008)
           return None
       user = verify_token(token= f"Bearer {token}", token_type="access")
       return user["id"]

    async def connect(self , user_id , websocket):
        self.connections[user_id].append(websocket)
        print("Websocket connected with" + user_id)


    async def disconnect(self , user_id , websocket):
        if user_id in self.connections:
            if websocket in self.connections[user_id]:
                self.connections[user_id].remove(websocket)
            if len(self.connections[user_id]) == 0:
                del self.connections[user_id]

    async def send_message(self , websocket, user_id , message , add_task_use_case : AddTaskUseCase ,
                           update_task_use_case : UpdateTaskUseCase , delete_task_use_case : DeleteTaskUseCase):
        try:
            type = message["type"]
            task = message["task"]
            if task and not task["userId"]:
              task["userId"] = user_id
            print(task)
            if type == "task":
              await add_task_use_case.execute(TaskDTO(**task))
            elif type == "update_task":
                await update_task_use_case.execute(task)
            elif type == "delete_task":
                await delete_task_use_case.execute(task)
            for connection in self.connections[user_id]:
                await connection.send_json(WebsocketMessage(type=type, task=task , error=None).model_dump())
        except Exception as e:
            await websocket.send_json(WebsocketMessage(type="error" , task= None , error=str(e)).model_dump())
connection_repo_impl = ConnectionRepoImpl()


