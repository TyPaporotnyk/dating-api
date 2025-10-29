from dataclasses import dataclass
from uuid import UUID

from dating.auth.repositories.base import BaseUserRepository
from dating.database.managers.base import TransactionManager
from dating.filters.commands import CreateProfileFilterCommand
from dating.filters.entities import ProfileFilter
from dating.filters.exceptions import ProfileFilterAlreadyExists
from dating.filters.repositories.base import BaseProfileFilterRepository


@dataclass
class CreateProfileFilterInteractor:
    user_repository: BaseUserRepository
    profile_filter_repository: BaseProfileFilterRepository
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID, command: CreateProfileFilterCommand) -> ProfileFilter:
        await self.user_repository.try_get_by_id(user_id=user_id)

        if await self.profile_filter_repository.get_by_user_id(user_id=user_id):
            raise ProfileFilterAlreadyExists

        profile_filter = ProfileFilter(
            user_id=user_id,
            gender_preference=command.gender_preference,
            age_min=command.age_min,
            age_max=command.age_max,
            max_distance_meters=command.max_distance_meters,
            show_only_with_photos=command.show_only_with_photos,
        )

        await self.profile_filter_repository.create(profile_filter)
        await self.transaction_manager.commit()

        return profile_filter
