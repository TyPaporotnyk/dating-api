from uuid import UUID
from fastapi import APIRouter, UploadFile, File
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from dating.auth.dependencies import CurrentUser
from dating.config import MEDIA_DIR
from dating.photos.commands import CreateProfilePhotoCommand
from dating.photos.interactors.create import CreateProfilePhotoInteractor
from dating.photos.interactors.delete import DeleteProfilePhotoInteractor
from dating.photos.interactors.get_all import GetAllProfilePhotoInteractor
from dating.photos.repositories.base import BaseProfileImageRepository
from dating.photos.schemas import BaseProfilePhotoSchema
from dating.utils.files import validate_file_size_type

router = APIRouter(route_class=DishkaRoute)


@router.post("", response_model=BaseProfilePhotoSchema)
async def upload_photo(
    current_user_id: CurrentUser,
    interactor: FromDishka[CreateProfilePhotoInteractor],
    file: UploadFile = File(...),
):
    validate_file_size_type(file)
    command = CreateProfilePhotoCommand(file=await file.read())
    profile_photo = await interactor(user_id=current_user_id, command=command)

    return BaseProfilePhotoSchema.from_dto(profile_photo)


@router.get("", response_model=list[BaseProfilePhotoSchema])
async def get_all_photos(
    current_user_id: CurrentUser, interactor: FromDishka[GetAllProfilePhotoInteractor]
):
    profile_photos = await interactor(user_id=current_user_id)

    return [BaseProfilePhotoSchema.from_dto(profile_photo) for profile_photo in profile_photos]


@router.delete("/{image_id}")
async def delete_photo(
    image_id: UUID,
    current_user_id: CurrentUser,
    interactor: FromDishka[DeleteProfilePhotoInteractor],
):
    await interactor(user_id=current_user_id, image_id=image_id)
