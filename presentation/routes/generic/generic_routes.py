from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.params import Cookie

from data.helpers.exceptions import TokenExpiredException
from data.helpers.generics import rotate_token
from data.helpers.jwt_auth import verify_token, create_access_token

gen_router = APIRouter()

@gen_router.get("/")
async def test():
    return {"message" : "connected"}
@gen_router.get("/refresh_token")
async def refresh_token_route(request : Request):
    ref_token_with_scheme = request.headers.get("Authorization")
    print(f"Receiving {ref_token_with_scheme}")
    try:
        new_token = await rotate_token(ref_token_with_scheme)
        return {"new_token": new_token}
    except Exception as e:
        print("Exception at rotation is" +  str(e))
        raise HTTPException(status_code=500 , detail=str(e))

@gen_router.get("/get_session")
async def get_session(request : Request):
    try:
      ref_token = request.headers.get("Authorization")
      if not ref_token:
          raise HTTPException(status_code=404 , detail="session not found")
      print(f"header is {ref_token}")
      user = verify_token(token_with_scheme=ref_token ,token_type="refresh")
      return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500 , detail=str(e))

