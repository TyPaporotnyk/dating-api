from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from dating.filters.entities import ProfileFilter
from dating.filters.exceptions import FilterNotFound
from dating.filters.models import ProfileFilterModel
from dating.filters.repositories.base import BaseProfileFilterRepository


class SQLAlchemyProfileFilterRepository(BaseProfileFilterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, profile_filter: ProfileFilter):
        profile_filter_model = ProfileFilterModel.from_entity(profile_filter)
        self.session.add(profile_filter_model)

    async def get_by_user_id(self, user_id: UUID) -> ProfileFilter | None:
        query = select(ProfileFilterModel).where(ProfileFilterModel.user_id == user_id)
        result = await self.session.execute(query)
        profile_filter_model = result.scalar_one_or_none()
        return profile_filter_model.to_entity() if profile_filter_model else None

    async def try_get_by_user_id(self, user_id: UUID) -> ProfileFilter:
        profile_filter = await self.get_by_user_id(user_id=user_id)
        if not profile_filter:
            raise FilterNotFound

        return profile_filter

    async def update(self, profile_filter: ProfileFilter):
        query = (
            update(ProfileFilterModel)
            .where(ProfileFilterModel.id == profile_filter.id)
            .values(
                gender_preference=profile_filter.gender_preference,
                age_min=profile_filter.age_min,
                age_max=profile_filter.age_max,
                max_distance_meters=profile_filter.max_distance_meters,
                show_only_with_photos=profile_filter.show_only_with_photos,
            )
        )
        await self.session.execute(query)
