from dataclasses import dataclass
from uuid import UUID

from dating.auth.repositories.base import BaseUserRepository
from dating.database.managers.base import TransactionManager
from dating.enums import InteractionType
from dating.interactions.entities import Interaction
from dating.interactions.repositories.base import BaseInteractionRepository


@dataclass
class CreateInteractionInteractor:
    user_repository: BaseUserRepository
    interaction_repository: BaseInteractionRepository
    transaction_manager: TransactionManager

    async def __call__(
        self, from_user_id: UUID, to_user_id: UUID, interaction_type: InteractionType
    ) -> Interaction:
        await self.user_repository.try_get_by_id(user_id=from_user_id)
        await self.user_repository.try_get_by_id(user_id=to_user_id)

        reverse_interaction = await self.interaction_repository.get_interaction(
            from_user_id=to_user_id, to_user_id=from_user_id
        )

        interaction = Interaction(
            from_user_id=from_user_id, to_user_id=to_user_id, interaction_type=interaction_type
        )

        if (
            interaction_type == InteractionType.LIKE
            and reverse_interaction
            and reverse_interaction.interaction_type == InteractionType.LIKE
        ):
            interaction.make_match()
            reverse_interaction.make_match()

            await self.interaction_repository.update(reverse_interaction)

        await self.interaction_repository.create(interaction)
        await self.transaction_manager.commit()

        return interaction
