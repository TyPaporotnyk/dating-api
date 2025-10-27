from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dating.auth.entities import User
from dating.auth.exceptions import UserNotFound
from dating.auth.models import UserModel
from dating.auth.repositories.base import BaseUserRepository


class SQLAlchemyUserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> None:
        user_model = UserModel.from_entity(user)
        self.session.add(user_model)

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def try_get_by_id(self, user_id: UUID) -> User:
        user = await self.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFound

        return user

    async def get_by_email(self, email: str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None
