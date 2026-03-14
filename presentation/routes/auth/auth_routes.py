from fastapi import FastAPI, APIRouter, Depends, Body, HTTPException
from starlette.responses import JSONResponse

from data.helpers.exceptions import UseCaseException
from data.models.user_model import User
from data.schemas.user_schema import Sign_In_Request, User_Schema, Sign_Up_Request
from domain.usecases.auth.LogUserInUseCase import LogUserInUseCase
from domain.usecases.auth.RegisterUserUseCase import RegisterUserUseCase
from presentation.deps.dependencies import get_auth_use_case, log_in_use_case

auth_router = APIRouter()

@auth_router.post("/sign_up")
async def sign_up(req : Sign_Up_Request = Body(...), usecase : RegisterUserUseCase = Depends(get_auth_use_case)):
   user = User(name = req.name , email=req.email , password=req.password, profile="")
   try:
       tokens = await usecase.execute(user)
       return JSONResponse(status_code=200 , content={
                "accessToken" : tokens[0] ,
                "refreshToken" : tokens[1] ,
                "userId" : tokens[2]
            })
   except Exception as e:
       print(e)
       return HTTPException(status_code=500, detail=str(e))

@auth_router.post("/sign_in")
async def sign_in(req : Sign_In_Request = Body(...) ,  usecase : LogUserInUseCase = Depends(log_in_use_case)):
   try:
       tokens = await usecase.execute(req.email , req.password)
       return JSONResponse(status_code=200 , content={
           "accessToken" : tokens[0] ,
           "refreshToken" : tokens[1] ,
           "userId" : tokens[2]
       })
   except UseCaseException as e:
       raise HTTPException(status_code=404, detail=e.args[0])
   except Exception as e:
       print(e)
       raise HTTPException(status_code=500, detail=str(e))
