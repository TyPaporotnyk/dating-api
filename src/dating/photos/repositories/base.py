from typing import Protocol
from uuid import UUID

from dating.photos.entities import ProfilePhoto


class BaseProfileImageRepository(Protocol):
    async def create(self, profile_photo: ProfilePhoto) -> None: ...

    async def get_all(self, profile_id: UUID) -> list[ProfilePhoto]: ...

    async def delete(self, photo_id: UUID): ...
