from dataclasses import dataclass
from uuid import UUID

from dating.database.managers.base import TransactionManager
from dating.profiles.commands import UpdateProfileCommand
from dating.profiles.entities import Profile
from dating.profiles.repositories.base import BaseProfileRepository


@dataclass
class UpdateProfileInteractor:
    profile_repository: BaseProfileRepository
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID, command: UpdateProfileCommand) -> Profile:
        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)

        profile.first_name = command.first_name
        profile.last_name = command.last_name
        profile.age = command.age
        profile.gender = command.gender

        await self.profile_repository.update(profile)
        await self.transaction_manager.commit()

        return profile
