from dataclasses import dataclass
from uuid import UUID

from dating.entities import Entity
from dating.enums import InteractionType


@dataclass
class Interaction(Entity):
    first_user_id: UUID | None
    second_user_id: UUID | None

    first_user_interaction_type: InteractionType | None
    second_user_interaction_type: InteractionType | None
