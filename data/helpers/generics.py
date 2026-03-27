from typing import Optional
from data.helpers.jwt_auth import verify_token, create_access_token
from fastapi import Request
async def rotate_token(token : Optional[str] , token_with_scheme : Optional[str]):
    if token_with_scheme and token:
        return None
    else:
        payload = verify_token(token=token, token_type="refresh")
        new_token = create_access_token(payload)
        return new_token