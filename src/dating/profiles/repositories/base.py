from typing import Protocol
from uuid import UUID

from dating.profiles.entities import Profile


class BaseProfileRepository(Protocol):
    async def create(self, profile: Profile) -> None: ...

    async def get_by_user_id(self, user_id: UUID) -> Profile | None: ...

    async def try_get_by_user_id(self, user_id: UUID) -> Profile: ...
