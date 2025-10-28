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
class GetAllProfilePhotoInteractor:
    profile_repository: BaseProfileRepository
    profile_image_repository: BaseProfileImageRepository

    async def __call__(self, user_id: UUID) -> list[ProfilePhoto]:
        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)
        return await self.profile_image_repository.get_all(profile_id=profile.id)
