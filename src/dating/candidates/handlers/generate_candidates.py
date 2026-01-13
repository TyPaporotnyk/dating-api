import logging
from dataclasses import dataclass

from dating.candidates.events import GenerateCandidatesPoolEvent
from dating.candidates.pools import CandidatePool
from dating.candidates.repositories.base import BaseCandidatesRepository
from dating.config import CANDIDATES_GEN_SIZE
from dating.filters.repositories.base import BaseProfileFilterRepository
from dating.mediator.events.handlers import BaseEventHandler
from dating.profiles.repositories.base import BaseProfileRepository

logger = logging.getLogger(__name__)


@dataclass
class GenerateCandidatesPoolEventHandler(BaseEventHandler[GenerateCandidatesPoolEvent, None]):
    profile_repository: BaseProfileRepository
    profile_filter_repository: BaseProfileFilterRepository
    candidates_repository: BaseCandidatesRepository
    candidate_pool: CandidatePool

    async def handle(self, event: GenerateCandidatesPoolEvent) -> None:
        logger.info("Generating candidates for user %s", event.user_id)
        profile = await self.profile_repository.try_get_by_user_id(user_id=event.user_id)
        profile_filter = await self.profile_filter_repository.try_get_by_user_id(
            user_id=event.user_id
        )

        candidates = await self.candidates_repository.get_candidates(
            current_user_profile=profile,
            current_user_filter=profile_filter,
            size=CANDIDATES_GEN_SIZE,
        )

        await self.candidate_pool.put_to_pool(key=str(event.user_id), obj=candidates)
