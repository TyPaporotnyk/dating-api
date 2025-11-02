import logging
from dataclasses import dataclass
from uuid import UUID

from dating.auth.repositories.base import BaseUserRepository
from dating.candidates.entities import Candidate
from dating.candidates.pools import CandidatePool
from dating.candidates.repositories.base import BaseCandidatesRepository
from dating.config import CANDIDATES_GEN_SIZE, CANDIDATES_MIN_POOL_SIZE
from dating.filters.repositories.base import BaseProfileFilterRepository
from dating.profiles.repositories.base import BaseProfileRepository

logger = logging.getLogger(__name__)


@dataclass
class CandidateFeedService:
    user_repository: BaseUserRepository
    profile_repository: BaseProfileRepository
    profile_filter_repository: BaseProfileFilterRepository
    candidates_repository: BaseCandidatesRepository
    candidate_pool: CandidatePool

    async def next_candidate(self, user_id: UUID) -> Candidate | None:
        await self.user_repository.try_get_by_id(user_id=user_id)
        candidate = await self.candidate_pool.next_from_pool(key=str(user_id))
        candidates_pool_size = await self.get_candidate_pool_size(user_id=user_id)

        if candidates_pool_size <= CANDIDATES_MIN_POOL_SIZE:
            # Throw event to message brocker and generate new candidates to user
            logger.info("Sent event to generate candidates pool for user")

        return candidate

    async def generate_candidates(self, user_id: UUID):
        await self.user_repository.try_get_by_id(user_id=user_id)

        profile = await self.profile_repository.try_get_by_user_id(user_id=user_id)
        profile_filter = await self.profile_filter_repository.try_get_by_user_id(user_id=user_id)

        candidates = await self.candidates_repository.get_candidates(
            current_user_profile=profile,
            current_user_filter=profile_filter,
            size=CANDIDATES_GEN_SIZE,
        )

        await self.candidate_pool.put_to_pool(key=str(user_id), obj=candidates)

    async def get_candidate_pool_size(self, user_id: UUID) -> int:
        return await self.candidate_pool.get_pool_size(key=str(user_id))
