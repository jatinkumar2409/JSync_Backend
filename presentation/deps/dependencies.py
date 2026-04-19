from fastapi import Depends

from data.helpers.db import getdb
from data.impls.auth.AuthRepositoryImpl import AuthRepositoryImpl
from data.impls.auth.TokenRepositoryImpl import TokenRepositoryImpl
from data.impls.tasks.ConnectionRepoImpl import ConnectionRepoImpl, connection_repo_impl
from data.impls.tasks.TaskCompletionRepoImpl import TaskCompletionRepoImpl
from data.impls.tasks.TaskRepositoryImpl import TaskRepositoryImpl
from domain.usecases.auth.LogUserInUseCase import LogUserInUseCase
from domain.usecases.auth.RegisterUserUseCase import RegisterUserUseCase
from domain.usecases.tasks.AddTaskUseCase import AddTaskUseCase
from domain.usecases.tasks.DeleteTaskUseCase import DeleteTaskUseCase
from domain.usecases.tasks.GetTasksUseCase import GetTasksUseCase
from domain.usecases.tasks.UpdateTaskUseCase import UpdateTaskUseCase
from domain.usecases.tasks.task_completions.AddTaskCompletionUseCase import AddTaskCompletionUseCase
from domain.usecases.tasks.task_completions.DeleteTaskCompletionUseCase import DeleteTaskCompletionUseCase
from domain.usecases.tasks.task_completions.LoadTaskCompletionsUseCase import LoadTaskCompletions


def get_user_repo():
    return AuthRepositoryImpl()

def get_token_repo():
    return TokenRepositoryImpl()

def get_task_repo():
    return TaskRepositoryImpl()

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

def get_task_completion_repo():
    return TaskCompletionRepoImpl()

def add_task_completion_use_case(repo = Depends(get_task_completion_repo)):
    return AddTaskCompletionUseCase(repo)

def delete_task_completion_use_case(repo = Depends(get_task_completion_repo)):
    return DeleteTaskCompletionUseCase(repo)

def get_task_completions_use_case(repo = Depends(get_task_completion_repo)):
    return LoadTaskCompletions(repo)