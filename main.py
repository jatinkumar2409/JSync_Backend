from fastapi import FastAPI
from presentation.routes.auth.auth_routes import auth_router
from presentation.routes.generic.generic_routes import gen_router
from presentation.routes.tasks.ask_ai_routes import ask_ai_router
from presentation.routes.tasks.task_completion_routes import task_completion_router
from presentation.routes.tasks.task_routes import task_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost:3000",   # Next.js frontend
    "http://127.0.0.1:3000",
    "https://jolliest-deedra-hawkish.ngrok-free.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # allowed domains
    allow_credentials=True,       # cookies / auth headers
    allow_methods=["*"],          # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],          # all headers
)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(gen_router)
app.include_router(ask_ai_router)
app.include_router(task_completion_router)
@app.get("/")
def read_root():
    return {"Hello": "World"}
