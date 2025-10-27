from uuid import UUID
from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from dating.users.commands.create_user import CreateUserCommand
from dating.users.interactors.create_user import CreateUserInteractor
from dating.users.repositories.base import BaseUserRepository
from dating.users.schemas import CreateUserSchema, ResponseUserSchema

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=ResponseUserSchema)
async def create_user(data: CreateUserSchema, interaction: FromDishka[CreateUserInteractor]):
    command = CreateUserCommand(**data.model_dump())
    user = await interaction(command=command)
    return ResponseUserSchema.from_dto(user)


@router.get("/{user_id}", response_model=ResponseUserSchema)
async def get_user(user_id: UUID, repository: FromDishka[BaseUserRepository]):
    user = await repository.try_get_by_id(user_id=user_id)
    return ResponseUserSchema.from_dto(user)
