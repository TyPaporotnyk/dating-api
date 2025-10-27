from typing import Protocol
from uuid import UUID

from dating.profiles.entities import Profile


class BaseProfileRepository(Protocol):
    async def create(self, profile: Profile): ...

    async def get_by_user_id(self, user_id: UUID) -> Profile | None: ...

    async def try_get_by_user_id(self, user_id: UUID) -> Profile: ...

    async def update(self, profile: Profile): ...
