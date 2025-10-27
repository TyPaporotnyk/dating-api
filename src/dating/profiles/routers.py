from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from dating.auth.dependencies import CurrentUser
from dating.profiles.commands import CreateProfileCommand
from dating.profiles.interactors.create import CreateProfileInteractor
from dating.profiles.repositories.base import BaseProfileRepository
from dating.profiles.schemas import CreateProfileSchema, ResponseProfileSchema


router = APIRouter(route_class=DishkaRoute)


@router.get("/", response_model=ResponseProfileSchema)
async def get_user_profile(user_id: CurrentUser, repository: FromDishka[BaseProfileRepository]):
    profile = await repository.try_get_by_user_id(user_id=user_id)
    return ResponseProfileSchema.from_dto(profile)


@router.post("/", response_model=ResponseProfileSchema)
async def create_user_profile(
    user_id: CurrentUser, data: CreateProfileSchema, interactor: FromDishka[CreateProfileInteractor]
):
    command = CreateProfileCommand(user_id=user_id, **data.model_dump())
    profile = await interactor(command)
    return ResponseProfileSchema.from_dto(profile)
