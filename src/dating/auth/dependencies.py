from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dating.auth.exceptions import AuthError
from dating.auth.services.jwt import JWTService
from dating.dependencies.container import container

bearer_schema = HTTPBearer()


async def get_jwt_service() -> JWTService:
    return await container.get(JWTService)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> UUID:
    jwt_token = credentials.credentials

    payload = jwt_service.validate_token(jwt_token)

    if payload.type != "access":
        raise AuthError

    if not payload.sub:
        raise AuthError

    user_id = payload.sub

    return user_id


CurrentUser = Annotated[UUID, Depends(get_current_user)]
