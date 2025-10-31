from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dating.auth.repositories.base import BaseUserRepository
from dating.auth.services.jwt import JWTService
from dating.dependencies.container import container

bearer_schema = HTTPBearer()


async def get_jwt_service() -> JWTService:
    return await container.get(JWTService)


async def get_user_repository() -> BaseUserRepository:
    return await container.get(BaseUserRepository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
    # jwt_service: JWTService = Depends(get_jwt_service),
    user_repository: BaseUserRepository = Depends(get_user_repository),
) -> int:
    # jwt_token = credentials.credentials

    # payload = await jwt_service.validate_token(jwt_token)

    # if payload.type != "access":
    #     raise AuthError

    # if not payload.sub:
    #     raise AuthError

    # user_id = payload.sub

    return 1


CurrentUser = Annotated[UUID, Depends(get_current_user)]
