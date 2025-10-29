from uuid import UUID

from geoalchemy2.shape import from_shape
from shapely import Point as SH_Point
from sqlalchemy import select, update
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

    async def update(self, profile: Profile):
        location = None
        if profile.location:
            sh_point = SH_Point(profile.location.latitude, profile.location.longitude)
            location = from_shape(sh_point, srid=4326)

        query = (
            update(ProfileModel)
            .where(ProfileModel.id == profile.id)
            .values(
                first_name=profile.first_name,
                last_name=profile.last_name,
                age=profile.age,
                gender=profile.gender,
                user_id=profile.user_id,
                location=location,
            )
        )
        await self.session.execute(query)
