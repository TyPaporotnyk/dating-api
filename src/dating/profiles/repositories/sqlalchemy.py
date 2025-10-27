from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dating.profiles.entities import Profile
from dating.profiles.exceptions import ProfileNotFound
from dating.profiles.models import ProfileModel
from dating.profiles.repositories.base import BaseProfileRepository


class SQLAlchemyProfileRepository(BaseProfileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, profile: Profile) -> None:
        profile_model = ProfileModel.from_entity(profile)
        self.session.add(profile_model)

    async def get_by_user_id(self, user_id: UUID) -> Profile | None:
        query = select(ProfileModel).where(ProfileModel.user_id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def try_get_by_user_id(self, user_id: UUID) -> Profile:
        profile = await self.get_by_user_id(user_id=user_id)
        if not profile:
            raise ProfileNotFound

        return profile
