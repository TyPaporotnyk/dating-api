from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dating.auth.exceptions import AuthError
from dating.utils.jwt import validate_jwt_token

bearer_schema = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
) -> UUID:
    jwt_token = credentials.credentials

    user_id = validate_jwt_token(jwt_token)
    if not user_id:
        raise AuthError

    return user_id


CurrentUser = Annotated[UUID, Depends(get_current_user)]
