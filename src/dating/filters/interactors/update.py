from dataclasses import dataclass
from uuid import UUID

from dating.database.managers.base import TransactionManager
from dating.filters.commands import UpdateProfileFilterCommand
from dating.filters.entities import ProfileFilter
from dating.filters.repositories.base import BaseProfileFilterRepository


@dataclass
class UpdateProfileFilterInteractor:
    profile_filter_repository: BaseProfileFilterRepository
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID, command: UpdateProfileFilterCommand) -> ProfileFilter:
        profile_filter = await self.profile_filter_repository.try_get_by_user_id(user_id=user_id)

        profile_filter.gender_preference = command.gender_preference
        profile_filter.age_min = command.age_min
        profile_filter.age_max = command.age_max
        profile_filter.max_distance_meters = command.max_distance_meters
        profile_filter.show_only_with_photos = command.show_only_with_photos

        await self.profile_filter_repository.update(profile_filter)
        await self.transaction_manager.commit()

        return profile_filter
