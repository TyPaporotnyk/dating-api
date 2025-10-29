from typing import Protocol
from uuid import UUID

from dating.filters.entities import ProfileFilter


class BaseProfileFilterRepository(Protocol):
    async def create(self, profile_filter: ProfileFilter): ...

    async def get_by_user_id(self, user_id: UUID) -> ProfileFilter | None: ...

    async def try_get_by_user_id(self, user_id: UUID) -> ProfileFilter: ...

    async def update(self, profile_filter: ProfileFilter): ...
