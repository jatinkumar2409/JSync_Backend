from fastapi import Depends

from data.helpers.db import getdb
from data.impls.auth.AuthRepositoryImpl import AuthRepositoryImpl
from data.impls.auth.TokenRepositoryImpl import TokenRepositoryImpl
from data.impls.tasks.ConnectionRepoImpl import ConnectionRepoImpl, connection_repo_impl
from data.impls.tasks.TaskRepositoryImpl import TaskRepositoryImpl
from domain.usecases.auth.LogUserInUseCase import LogUserInUseCase
from domain.usecases.auth.RegisterUserUseCase import RegisterUserUseCase
from domain.usecases.tasks.AddTaskUseCase import AddTaskUseCase
from domain.usecases.tasks.DeleteTaskUseCase import DeleteTaskUseCase
from domain.usecases.tasks.GetTasksUseCase import GetTasksUseCase
from domain.usecases.tasks.UpdateTaskUseCase import UpdateTaskUseCase


def get_user_repo(db = Depends(getdb)):
    return AuthRepositoryImpl(db)

def get_token_repo(db = Depends(getdb)):
    return TokenRepositoryImpl(db)

def get_task_repo(db = Depends(getdb)):
    return TaskRepositoryImpl(db)

def get_auth_use_case(repo = Depends(get_user_repo) , token_repo = Depends(get_token_repo)):
    return RegisterUserUseCase(repo , token_repo)

def log_in_use_case(repo = Depends(get_user_repo) , token_repo = Depends(get_token_repo)):
    return LogUserInUseCase(repo , token_repo)

def add_task_use_case(repo = Depends(get_task_repo)):
    return AddTaskUseCase(repo)
def get_tasks_use_case(repo = Depends(get_task_repo)):
    return GetTasksUseCase(repo)
def update_task_use_case(repo = Depends(get_task_repo)):
    return UpdateTaskUseCase(repo)
def delete_task_use_case(repo = Depends(get_task_repo)):
    return DeleteTaskUseCase(repo)


def get_task_connection_repo():
    return connection_repo_impl
