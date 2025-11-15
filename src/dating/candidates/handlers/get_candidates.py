import logging
from dataclasses import dataclass

from dating.candidates.commands import GetNextCandidateCommand
from dating.candidates.entities import Candidate
from dating.candidates.events import GenerateCandidatesPoolEvent
from dating.candidates.pools import CandidatePool
from dating.config import CANDIDATES_MIN_POOL_SIZE
from dating.mediator.commands.handlers import BaseCommandHandler

logger = logging.getLogger(__name__)


@dataclass
class GetNextCandidateCommandHandler(BaseCommandHandler[GetNextCandidateCommand, Candidate | None]):
    candidate_pool: CandidatePool

    async def handle(self, command: GetNextCandidateCommand) -> Candidate | None:
        logger.info("Get next candidate to user %s", command.user_id)
        pool_key = str(command.user_id)
        candidate = await self.candidate_pool.next_from_pool(key=pool_key)
        candidate_pool_size = await self.candidate_pool.get_pool_size(pool_key)

        if candidate_pool_size <= CANDIDATES_MIN_POOL_SIZE:
            event = GenerateCandidatesPoolEvent(user_id=command.user_id)
            await self._mediator.publish([event])

        return candidate
