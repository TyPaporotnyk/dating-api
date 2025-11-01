from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dating.auth.entities import User
from dating.auth.exceptions import AuthError
from dating.auth.repositories.base import BaseUserRepository
from dating.auth.repositories.sqlalchemy import SQLAlchemyUserRepository
from dating.auth.services.jwt import JWTService
from dating.database.dependencies import DbSessionDep
from dating.dependencies.container import container

bearer_schema = HTTPBearer()


async def get_jwt_service() -> JWTService:
    return await container.get(JWTService)


def get_user_repository(db_session: DbSessionDep) -> BaseUserRepository:
    return SQLAlchemyUserRepository(session=db_session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
    jwt_service: JWTService = Depends(get_jwt_service),
    user_repository: BaseUserRepository = Depends(get_user_repository),
) -> User:
    jwt_token = credentials.credentials

    payload = await jwt_service.validate_token(jwt_token)

    if payload.type != "access":
        raise AuthError

    if not payload.sub:
        raise AuthError

    user_id = payload.sub
    user = await user_repository.try_get_by_id(user_id=user_id)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
