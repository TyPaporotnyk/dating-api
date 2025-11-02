from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from dating.auth.dependencies import CurrentUser
from dating.profiles.commands import (
    CreateProfileCommand,
    UpdateProfileCommand,
    UpdateProfileLocationCommand,
)
from dating.profiles.interactors.create import CreateProfileInteractor
from dating.profiles.interactors.update import UpdateProfileInteractor
from dating.profiles.interactors.update_location import UpdateProfileLocationInteractor
from dating.profiles.repositories.base import BaseProfileRepository
from dating.profiles.schemas import (
    CreateProfileSchema,
    ResponseProfileSchema,
    UpdateProfileLocationSchema,
    UpdateProfileSchema,
)
from dating.schemas import ApiResponse
from dating.value_objects import Coordinates

router = APIRouter(route_class=DishkaRoute, tags=["profiles"])


@router.get("", response_model=ApiResponse[ResponseProfileSchema])
async def get_user_profile(
    user: CurrentUser, repository: FromDishka[BaseProfileRepository]
) -> ApiResponse[ResponseProfileSchema]:
    profile = await repository.try_get_by_user_id(user_id=user.id)
    return ApiResponse(data=ResponseProfileSchema.from_dto(profile))


@router.post("", response_model=ApiResponse[ResponseProfileSchema])
async def create_user_profile(
    user: CurrentUser, data: CreateProfileSchema, interactor: FromDishka[CreateProfileInteractor]
) -> ApiResponse[ResponseProfileSchema]:
    command = CreateProfileCommand(**data.model_dump())
    profile = await interactor(user_id=user.id, command=command)
    return ApiResponse(data=ResponseProfileSchema.from_dto(profile))


@router.put("", response_model=ApiResponse[ResponseProfileSchema])
async def update_user_profile(
    user: CurrentUser, data: UpdateProfileSchema, interactor: FromDishka[UpdateProfileInteractor]
) -> ApiResponse[ResponseProfileSchema]:
    command = UpdateProfileCommand(**data.model_dump())
    profile = await interactor(user_id=user.id, command=command)
    return ApiResponse(data=ResponseProfileSchema.from_dto(profile))


@router.patch("/location", response_model=ApiResponse[ResponseProfileSchema])
async def update_user_profile_location(
    user: CurrentUser,
    data: UpdateProfileLocationSchema,
    interactor: FromDishka[UpdateProfileLocationInteractor],
) -> ApiResponse[ResponseProfileSchema]:
    command = UpdateProfileLocationCommand(Coordinates(**data.model_dump()))
    profile = await interactor(user_id=user.id, command=command)
    return ApiResponse(data=ResponseProfileSchema.from_dto(profile))
