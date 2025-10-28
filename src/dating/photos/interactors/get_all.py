from dataclasses import dataclass
from uuid import UUID

from dating.photos.entities import ProfilePhoto
from dating.photos.repositories.base import BaseProfileImageRepository
from dating.profiles.repositories.base import BaseProfileRepository


@dataclass
class GetAllProfilePhotoInteractor:
    profile_repository: BaseProfileRepository
    profile_image_repository: BaseProfileImageRepository

    async def __call__(self, user_id: UUID) -> list[ProfilePhoto]:
        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)
        return await self.profile_image_repository.get_all(profile_id=profile.id)
