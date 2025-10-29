from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dating.candidates.repositories.base import BaseCandidatesRepository
from dating.filters.entities import ProfileFilter
from dating.filters.models import ProfileFilterModel
from dating.profiles.entities import Profile
from dating.profiles.exceptions import ProfileLocationRequired
from dating.profiles.models import ProfileModel


class SQLAlchemyCandidatesRepository(BaseCandidatesRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_candidates(
        self, current_user_profile: Profile, current_user_filter: ProfileFilter
    ) -> list[Profile]:
        user_location = current_user_profile.location

        if not user_location:
            raise ProfileLocationRequired

        user_point = func.ST_SetSRID(
            func.ST_MakePoint(user_location.longitude, user_location.latitude), 4326
        )

        distance = func.ST_Distance(
            func.Geography(ProfileModel.location), func.Geography(user_point)
        )

        query = (
            select(ProfileModel)
            .join(ProfileFilterModel, ProfileFilterModel.user_id == ProfileModel.user_id)
            .where(ProfileModel.user_id != current_user_profile.user_id)
            .where(ProfileModel.gender == current_user_filter.gender_preference)
            .where(ProfileFilterModel.gender_preference == current_user_profile.gender)
            .where(
                ProfileModel.age.between(
                    current_user_filter.age_min,
                    current_user_filter.age_max,
                )
            )
            .where(
                (ProfileFilterModel.age_min <= current_user_profile.age)
                & (ProfileFilterModel.age_max >= current_user_profile.age)
            )
            .where(
                func.ST_DWithin(
                    func.Geography(ProfileModel.location),
                    func.Geography(user_point),
                    current_user_filter.max_distance_meters,
                )
            )
            .where(
                func.ST_DWithin(
                    func.Geography(user_point),
                    func.Geography(ProfileModel.location),
                    ProfileFilterModel.max_distance_meters,
                )
            )
            .order_by(distance)
            .limit(20)
        )

        result = await self.session.execute(query)
        rows = result.scalars().all()

        return [row.to_entity() for row in rows]
