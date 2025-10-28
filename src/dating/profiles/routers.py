from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from dating.auth.dependencies import CurrentUser
from dating.profiles.commands import CreateProfileCommand, UpdateProfileCommand
from dating.profiles.interactors.create import CreateProfileInteractor
from dating.profiles.interactors.update import UpdateProfileInteractor
from dating.profiles.repositories.base import BaseProfileRepository
from dating.profiles.schemas import CreateProfileSchema, ResponseProfileSchema, UpdateProfileSchema

router = APIRouter(route_class=DishkaRoute)


@router.get("", response_model=ResponseProfileSchema)
async def get_user_profile(
    user_id: CurrentUser, repository: FromDishka[BaseProfileRepository]
) -> ResponseProfileSchema:
    profile = await repository.try_get_by_user_id(user_id=user_id)
    return ResponseProfileSchema.from_dto(profile)


@router.post("", response_model=ResponseProfileSchema)
async def create_user_profile(
    user_id: CurrentUser, data: CreateProfileSchema, interactor: FromDishka[CreateProfileInteractor]
) -> ResponseProfileSchema:
    command = CreateProfileCommand(**data.model_dump())
    profile = await interactor(user_id=user_id, command=command)
    return ResponseProfileSchema.from_dto(profile)


@router.put("", response_model=ResponseProfileSchema)
async def update_user_profile(
    user_id: CurrentUser, data: UpdateProfileSchema, interactor: FromDishka[UpdateProfileInteractor]
) -> ResponseProfileSchema:
    command = UpdateProfileCommand(**data.model_dump())
    profile = await interactor(user_id=user_id, command=command)
    return ResponseProfileSchema.from_dto(profile)
