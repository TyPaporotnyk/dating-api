from dataclasses import dataclass
from uuid import UUID

from dating.database.managers.base import TransactionManager
from dating.photos.exceptions import ImageNotFound
from dating.photos.repositories.base import BaseProfileImageRepository
from dating.photos.storages.base import Storage
from dating.profiles.repositories.base import BaseProfileRepository


@dataclass
class DeleteProfilePhotoInteractor:
    profile_repository: BaseProfileRepository
    profile_image_repository: BaseProfileImageRepository
    storage: Storage
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID, image_id: UUID):
        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)
        image = await self.profile_image_repository.get_by_profile_id_and_image_id(
            profile_id=profile.id, image_id=image_id
        )
        if not image:
            raise ImageNotFound

        await self.profile_image_repository.delete(image_id=image_id)
        await self.storage.delete(image.url)

        await self.transaction_manager.commit()
