from dataclasses import dataclass
from uuid import UUID, uuid4

from dating.config import MEDIA_DIR
from dating.database.managers.base import TransactionManager
from dating.auth.entities import User
from dating.photos.commands import CreateProfilePhotoCommand
from dating.photos.entities import ProfilePhoto
from dating.photos.repositories.base import BaseProfileImageRepository
from dating.photos.storages.base import Storage
from dating.profiles.repositories.base import BaseProfileRepository


@dataclass
class CreateProfilePhotoInteractor:
    profile_repository: BaseProfileRepository
    profile_image_repository: BaseProfileImageRepository
    storage_manager: Storage
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID, command: CreateProfilePhotoCommand) -> ProfilePhoto:
        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)

        photo_path = MEDIA_DIR / f"user/{user_id}/profile/{profile.id}/images/"
        image_hash = f"{uuid4()}.jpg"

        photo_url = await self.storage_manager.upload(file=command.file, path=photo_path, file_name=image_hash)

        photo = ProfilePhoto(
            profile_id=profile.id,
            url=photo_url
        )

        await self.profile_image_repository.create(photo)
        await self.transaction_manager.commit()

        return photo
