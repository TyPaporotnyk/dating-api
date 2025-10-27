import logging

from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from dating.auth.commands import CreateUserCommand, LoginUserCommand
from dating.auth.dependencies import CurrentUser
from dating.auth.exceptions import AuthError, UserAlreadyExist, UserNotFound
from dating.auth.interactors.create_user import CreateUserInteractor
from dating.auth.interactors.login import LoginUserInteractor
from dating.auth.repositories.base import BaseUserRepository
from dating.auth.schemas import (
    CreateUserSchema,
    LoginUserResponse,
    LoginUserSchema,
    ResponseUserSchema,
)

logger = logging.getLogger(__name__)
auth_router = APIRouter(route_class=DishkaRoute)
user_router = APIRouter(route_class=DishkaRoute)


@auth_router.post("/register", response_model=LoginUserResponse)
async def create_user(data: CreateUserSchema, interaction: FromDishka[CreateUserInteractor]):
    command = CreateUserCommand(**data.model_dump())
    try:
        user = await interaction(command=command)
    except UserAlreadyExist as e:
        logger.warning("User already exist", extra={"email": command.email})
        raise e

    logger.info("User registered successfully", extra={"email": command.email})
    return LoginUserResponse.from_dto(user)


@auth_router.post("/login", response_model=LoginUserResponse)
async def login_user(data: LoginUserSchema, interactor: FromDishka[LoginUserInteractor]):
    command = LoginUserCommand(**data.model_dump())

    try:
        user = await interactor(command=command)
    except (UserNotFound, AuthError) as e:
        logger.warning("User login failed: invalid credentials", extra={"email": command.email})
        raise e

    logger.info("User login successfuly", extra={"email": command.email})
    return LoginUserResponse.from_dto(user)


@user_router.get("", response_model=ResponseUserSchema)
async def get_current_user(user_id: CurrentUser, repository: FromDishka[BaseUserRepository]):
    try:
        user = await repository.try_get_by_id(user_id=user_id)
    except UserNotFound as e:
        logger.warning("User not found", extra={"user_id": user_id})
        raise e
    return ResponseUserSchema.from_dto(user)
