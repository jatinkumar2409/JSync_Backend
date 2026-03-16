import time
from typing import Optional

from fastapi import HTTPException , Request
from jose import jwt, JWTError

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_SECONDS = 120 * 60

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

def verify_token(token : Optional[str] , token_with_scheme : Optional[str] , token_type : str = "access"):
    if not token and not token_with_scheme:
        raise HTTPException(status_code=401, detail="Token missing")
    if token_with_scheme and not token:
        try:
            scheme, token = token_with_scheme.split(" ")
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid auth scheme")

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != token_type:
                raise HTTPException(status_code=401, detail="Invalid token type")

            return payload  # contains sub, exp, etc.

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    elif token and not token_with_scheme:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != token_type:
                raise HTTPException(status_code=401, detail="Invalid token type")

            return payload  # contains sub, exp, etc.

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    return None




