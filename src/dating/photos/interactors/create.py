from dataclasses import dataclass
from uuid import UUID, uuid4
from pathlib import Path

from dating.database.managers.base import TransactionManager
from dating.photos.commands import CreateProfilePhotoCommand
from dating.photos.entities import ProfilePhoto
from dating.photos.repositories.base import BaseProfileImageRepository
from dating.photos.storages.base import Storage
from dating.profiles.repositories.base import BaseProfileRepository


@dataclass
class CreateProfilePhotoInteractor:
    profile_repository: BaseProfileRepository
    profile_image_repository: BaseProfileImageRepository
    storage: Storage
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID, command: CreateProfilePhotoCommand) -> ProfilePhoto:
        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)

        photo_path = f"users/{user_id}/profile/{profile.id}/images"
        image_name = f"{uuid4()}.jpg"

        photo_url = await self.storage.upload(
            file=command.file,
            path=photo_path,
            file_name=image_name,
        )

        photo = ProfilePhoto(
            profile_id=profile.id,
            url=photo_url,
        )

        await self.profile_image_repository.create(photo)
        await self.transaction_manager.commit()

        return photo
