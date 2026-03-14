from fastapi import FastAPI
from presentation.routes.auth.auth_routes import auth_router
from presentation.routes.tasks.task_routes import task_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(task_router)
@app.get("/")
def read_root():
    return {"Hello": "World"}
