from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, UploadFile

from dating.auth.dependencies import CurrentUser
from dating.photos.commands import CreateProfilePhotoCommand
from dating.photos.interactors.create import CreateProfilePhotoInteractor
from dating.photos.interactors.delete import DeleteProfilePhotoInteractor
from dating.photos.interactors.get_all import GetAllProfilePhotoInteractor
from dating.photos.schemas import BaseProfilePhotoSchema
from dating.schemas import ApiResponse
from dating.utils.files import validate_file_size_type

router = APIRouter(route_class=DishkaRoute, tags=["photos"])


@router.post("", response_model=ApiResponse[BaseProfilePhotoSchema])
async def upload_photo(
    current_user_id: CurrentUser,
    interactor: FromDishka[CreateProfilePhotoInteractor],
    file: UploadFile = File(...),
) -> ApiResponse[BaseProfilePhotoSchema]:
    validate_file_size_type(file)
    command = CreateProfilePhotoCommand(file=await file.read())
    profile_photo = await interactor(user_id=current_user_id, command=command)

    return ApiResponse(data=BaseProfilePhotoSchema.from_dto(profile_photo))


@router.get("", response_model=ApiResponse[list[BaseProfilePhotoSchema]])
async def get_all_photos(
    current_user_id: CurrentUser, interactor: FromDishka[GetAllProfilePhotoInteractor]
) -> ApiResponse[list[BaseProfilePhotoSchema]]:
    profile_photos = await interactor(user_id=current_user_id)

    return ApiResponse(
        data=[BaseProfilePhotoSchema.from_dto(profile_photo) for profile_photo in profile_photos]
    )


@router.delete("/{image_id}")
async def delete_photo(
    image_id: UUID,
    current_user_id: CurrentUser,
    interactor: FromDishka[DeleteProfilePhotoInteractor],
) -> None:
    await interactor(user_id=current_user_id, image_id=image_id)
