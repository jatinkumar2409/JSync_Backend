from typing import Optional
from data.helpers.jwt_auth import verify_token, create_access_token
from fastapi import Request
async def rotate_token(token_with_scheme : Optional[str]):
        payload = verify_token(token_with_scheme=token_with_scheme, token_type="refresh")
        new_token = create_access_token(payload)
        return new_token