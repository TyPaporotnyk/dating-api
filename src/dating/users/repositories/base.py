from typing import Protocol
from uuid import UUID

from dating.users.entities import User


class BaseUserRepository(Protocol):
    async def create(self, user: User) -> None: ...

    async def get_by_id(self, user_id: UUID) -> User | None: ...

    async def try_get_by_id(self, user_id: UUID) -> User: ...

    async def get_by_email(self, email: str) -> User | None: ...
