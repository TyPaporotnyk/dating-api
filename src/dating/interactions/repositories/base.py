from typing import Protocol
from uuid import UUID

from dating.interactions.entities import Interaction


class BaseInteractionRepository(Protocol):
    async def create(self, interaction: Interaction): ...

    async def get_interaction(
        self, first_user_id: UUID, second_user_id: UUID
    ) -> Interaction | None: ...

    async def update(self, interaction: Interaction): ...
