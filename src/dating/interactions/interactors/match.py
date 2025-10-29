import logging
from dataclasses import dataclass
from uuid import UUID

from dating.auth.repositories.base import BaseUserRepository
from dating.database.managers.base import TransactionManager
from dating.enums import InteractionType
from dating.interactions.entities import Interaction
from dating.interactions.repositories.base import BaseInteractionRepository

logger = logging.getLogger(__name__)


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

        first_user_id, second_user_id = sorted([from_user_id, to_user_id])

        interaction = await self.interaction_repository.get_interaction(
            first_user_id=first_user_id, second_user_id=second_user_id
        )

        if not interaction:
            interaction = Interaction(
                first_user_id=first_user_id,
                second_user_id=second_user_id,
                first_user_interaction_type=interaction_type
                if first_user_id == from_user_id
                else None,
                second_user_interaction_type=interaction_type
                if second_user_id == from_user_id
                else None,
            )
            await self.interaction_repository.create(interaction)

        else:
            if from_user_id == interaction.first_user_id:
                interaction.first_user_interaction_type = interaction_type
            else:
                interaction.second_user_interaction_type = interaction_type

            if (
                interaction.first_user_interaction_type == InteractionType.LIKE
                and interaction.second_user_interaction_type == InteractionType.LIKE
            ):
                # TODO: Need to create a notification system
                logger.info("Two users matched!!!")

            await self.interaction_repository.update(interaction)

        await self.transaction_manager.commit()

        return interaction
