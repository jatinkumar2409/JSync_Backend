import time
from typing import Optional

from fastapi import HTTPException , Request
from jose import jwt
from jose.exceptions import JWTError , ExpiredSignatureError

from data.helpers.exceptions import TokenExpiredException, TokenValidationException

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_SECONDS = 20
#to be for development only change it to 120 * 60 later

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        "type": "refresh"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token_with_scheme : str, token_type : str = "access"):
    if not token_with_scheme:
        raise TokenExpiredException
    try:
            scheme, token = token_with_scheme.split(" ")
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=402, detail="Invalid auth scheme")

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != token_type:
                raise TokenExpiredException

            return payload

    except ExpiredSignatureError:
            raise TokenExpiredException
    except JWTError:
            raise TokenValidationException






