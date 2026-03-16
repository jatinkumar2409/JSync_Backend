from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.params import Cookie

from data.helpers.generics import rotate_token

gen_router = APIRouter()

@gen_router.get("/refresh")
async def refresh_token(request : Request , refresh_token : str = Cookie(None)):
    ref_token_with_scheme = request.headers.get("Authorization")
    try:
       new_token = await rotate_token(refresh_token , ref_token_with_scheme)
       return {"new_token" : new_token}
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

