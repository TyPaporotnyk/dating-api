from typing import Protocol
from uuid import UUID

from dating.photos.entities import ProfilePhoto


class BaseProfileImageRepository(Protocol):
    async def create(self, profile_photo: ProfilePhoto) -> None: ...

    async def get_all(self, profile_id: UUID) -> list[ProfilePhoto]: ...

    async def get_by_profile_id_and_image_id(
        self, profile_id: UUID, image_id: UUID
    ) -> ProfilePhoto | None: ...

    async def delete(self, image_id: UUID): ...
