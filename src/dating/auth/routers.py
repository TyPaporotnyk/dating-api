from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from dating.auth.commands import CreateUserCommand, LoginUserCommand
from dating.auth.dependencies import CurrentUser
from dating.auth.interactors.create_user import CreateUserInteractor
from dating.auth.interactors.login import LoginUserInteractor
from dating.auth.repositories.base import BaseUserRepository
from dating.auth.schemas import (
    CreateUserSchema,
    LoginUserResponse,
    LoginUserSchema,
    ResponseUserSchema,
)

auth_router = APIRouter(route_class=DishkaRoute)
user_router = APIRouter(route_class=DishkaRoute)


@auth_router.post("/register", response_model=LoginUserResponse)
async def create_user(data: CreateUserSchema, interaction: FromDishka[CreateUserInteractor]):
    command = CreateUserCommand(**data.model_dump())
    user = await interaction(command=command)
    return LoginUserResponse.from_dto(user)


@auth_router.post("/login", response_model=LoginUserResponse)
async def login_user(data: LoginUserSchema, interactor: FromDishka[LoginUserInteractor]):
    command = LoginUserCommand(**data.model_dump())
    user = await interactor(command=command)
    return LoginUserResponse.from_dto(user)


@user_router.get("/me", response_model=ResponseUserSchema)
async def get_auth_user(user_id: CurrentUser, repository: FromDishka[BaseUserRepository]):
    user = await repository.try_get_by_id(user_id=user_id)
    return ResponseUserSchema.from_dto(user)
