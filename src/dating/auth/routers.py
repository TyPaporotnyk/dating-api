import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from dating.auth.commands import CreateUserCommand, LoginUserCommand
from dating.auth.dependencies import CurrentUser
from dating.auth.exceptions import AuthError, UserAlreadyExist, UserNotFound
from dating.auth.interactors.create_user import CreateUserInteractor
from dating.auth.interactors.login import LoginUserInteractor
from dating.auth.repositories.base import BaseUserRepository
from dating.auth.schemas import (
    CreateUserSchema,
    LoginUserSchema,
    RefreshTokenSchema,
    ResponseUserSchema,
    TokenPairResponse,
)
from dating.auth.services.jwt import JWTService
from dating.schemas import ApiResponse

logger = logging.getLogger(__name__)
auth_router = APIRouter(route_class=DishkaRoute, tags=["auth"])
user_router = APIRouter(route_class=DishkaRoute, tags=["users"])


@auth_router.post("/register", response_model=ApiResponse[TokenPairResponse])
async def create_user(
    data: CreateUserSchema, interaction: FromDishka[CreateUserInteractor]
) -> ApiResponse[TokenPairResponse]:
    command = CreateUserCommand(**data.model_dump())
    try:
        token_pair = await interaction(command=command)
    except UserAlreadyExist as e:
        logger.warning("User already exist", extra={"email": command.email})
        raise e

    logger.info("User registered successfully", extra={"email": command.email})
    return ApiResponse(data=TokenPairResponse.from_dto(token_pair))


@auth_router.post("/login", response_model=ApiResponse[TokenPairResponse])
async def login_user(
    data: LoginUserSchema, interactor: FromDishka[LoginUserInteractor]
) -> ApiResponse[TokenPairResponse]:
    command = LoginUserCommand(**data.model_dump())

    try:
        token_pair = await interactor(command=command)
    except (UserNotFound, AuthError) as e:
        logger.warning("User login failed: invalid credentials", extra={"email": command.email})
        raise e

    logger.info("User login successfully", extra={"email": command.email})
    return ApiResponse(data=TokenPairResponse.from_dto(token_pair))


@auth_router.post("/refresh", response_model=ApiResponse[TokenPairResponse])
async def refresh_token(
    data: RefreshTokenSchema, token_service: FromDishka[JWTService]
) -> ApiResponse[TokenPairResponse]:
    token_pair = await token_service.refresh_tokens(data.refresh_token)
    return ApiResponse(data=TokenPairResponse.from_dto(token_pair))


@user_router.get("", response_model=ApiResponse[ResponseUserSchema])
async def get_current_user(
    user_id: CurrentUser, repository: FromDishka[BaseUserRepository]
) -> ApiResponse[ResponseUserSchema]:
    try:
        user = await repository.try_get_by_id(user_id=user_id)
    except UserNotFound as e:
        logger.warning("User not found", extra={"user_id": user_id})
        raise e
    return ApiResponse(data=ResponseUserSchema.from_dto(user))
