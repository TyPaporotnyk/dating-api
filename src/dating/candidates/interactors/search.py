from dataclasses import dataclass
from uuid import UUID

from dating.auth.repositories.base import BaseUserRepository
from dating.candidates.repositories.base import BaseCandidatesRepository
from dating.filters.repositories.base import BaseProfileFilterRepository
from dating.profiles.entities import Profile
from dating.profiles.repositories.base import BaseProfileRepository


@dataclass
class SearchCandidatesInteractor:
    user_repository: BaseUserRepository
    profile_repository: BaseProfileRepository
    profile_filter_repository: BaseProfileFilterRepository
    candidates_repository: BaseCandidatesRepository

    async def __call__(self, user_id: UUID) -> list[Profile]:
        await self.user_repository.try_get_by_id(user_id=user_id)

        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)
        profile_filter = await self.profile_filter_repository.try_get_by_user_id(user_id=user_id)

        candidates = await self.candidates_repository.get_candidates(
            current_user_profile=profile, current_user_filter=profile_filter
        )

        return candidates
