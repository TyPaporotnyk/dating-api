from dataclasses import dataclass
from uuid import UUID

from dating.mediator.commands.entities import BaseCommand


@dataclass(frozen=True)
class GetNextCandidateCommand(BaseCommand):
    user_id: UUID
