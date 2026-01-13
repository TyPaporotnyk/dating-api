from dataclasses import dataclass
from uuid import UUID

from dating.mediator.events.entities import BaseEvent


@dataclass(frozen=True)
class GenerateCandidatesPoolEvent(BaseEvent):
    user_id: UUID
