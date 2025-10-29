from dataclasses import dataclass
from uuid import UUID

from dating.entities import Entity
from dating.enums import InteractionType


@dataclass
class Interaction(Entity):
    from_user_id: UUID
    to_user_id: UUID

    interaction_type: InteractionType

    is_match: bool = False

    def make_match(self):
        self.is_match = True
