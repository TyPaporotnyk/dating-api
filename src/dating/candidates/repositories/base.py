from typing import Protocol

from dating.filters.entities import ProfileFilter
from dating.profiles.entities import Profile


class BaseCandidatesRepository(Protocol):
    async def get_candidates(
        self, current_user_profile: Profile, current_user_filter: ProfileFilter
    ) -> list[Profile]: ...
