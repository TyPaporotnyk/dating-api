from dataclasses import dataclass

from dating.auth.repositories.base import BaseUserRepository
from dating.database.managers.base import TransactionManager
from dating.profiles.commands import CreateProfileCommand
from dating.profiles.entities import Profile
from dating.profiles.repositories.base import BaseProfileRepository


@dataclass
class CreateProfileInteractor:
    user_repository: BaseUserRepository
    profile_repository: BaseProfileRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: CreateProfileCommand) -> Profile:
        await self.user_repository.try_get_by_id(user_id=command.user_id)

        profile = Profile(
            first_name=command.first_name,
            last_name=command.last_name,
            age=command.age,
            gender=command.gender,
            user_id=command.user_id,
        )
        await self.profile_repository.create(profile)
        await self.transaction_manager.commit()

        return profile
