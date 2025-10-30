from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from dating.auth.dependencies import CurrentUser
from dating.filters.commands import CreateProfileFilterCommand, UpdateProfileFilterCommand
from dating.filters.interactors.create import CreateProfileFilterInteractor
from dating.filters.interactors.update import UpdateProfileFilterInteractor
from dating.filters.repositories.base import BaseProfileFilterRepository
from dating.filters.schemas import (
    CreateProfileFilterSchema,
    ResponseProfileFilterSchema,
    UpdateProfileFilterSchema,
)
from dating.schemas import ApiResponse

router = APIRouter(route_class=DishkaRoute, tags=["filters"])


@router.get("", response_model=ApiResponse[ResponseProfileFilterSchema])
async def get_user_filter(
    user_id: CurrentUser, repository: FromDishka[BaseProfileFilterRepository]
) -> ApiResponse[ResponseProfileFilterSchema]:
    filter = await repository.try_get_by_user_id(user_id=user_id)
    return ApiResponse(data=ResponseProfileFilterSchema.from_dto(filter))


@router.post("", response_model=ApiResponse[ResponseProfileFilterSchema])
async def create_user_filter(
    user_id: CurrentUser,
    data: CreateProfileFilterSchema,
    interactor: FromDishka[CreateProfileFilterInteractor],
) -> ApiResponse[ResponseProfileFilterSchema]:
    command = CreateProfileFilterCommand(**data.model_dump())
    filter = await interactor(user_id=user_id, command=command)
    return ApiResponse(data=ResponseProfileFilterSchema.from_dto(filter))


@router.put("", response_model=ApiResponse[ResponseProfileFilterSchema])
async def update_user_filter(
    user_id: CurrentUser,
    data: UpdateProfileFilterSchema,
    interactor: FromDishka[UpdateProfileFilterInteractor],
) -> ApiResponse[ResponseProfileFilterSchema]:
    command = UpdateProfileFilterCommand(**data.model_dump())
    filter = await interactor(user_id=user_id, command=command)
    return ApiResponse(data=ResponseProfileFilterSchema.from_dto(filter))
