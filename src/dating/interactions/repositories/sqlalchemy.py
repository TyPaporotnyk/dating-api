from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from dating.interactions.entities import Interaction
from dating.interactions.models import InteractionModel
from dating.interactions.repositories.base import BaseInteractionRepository


class SQLAlchemyInteractionRepository(BaseInteractionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, interaction: Interaction):
        interaction_model = InteractionModel.from_entity(interaction)
        self.session.add(interaction_model)

    async def get_interaction(
        self, first_user_id: UUID, second_user_id: UUID
    ) -> Interaction | None:
        query = select(InteractionModel).where(
            and_(
                InteractionModel.first_user_id == first_user_id,
                InteractionModel.second_user_id == second_user_id,
            )
        )
        result = await self.session.execute(query)
        interaction_model = result.scalar_one_or_none()
        return interaction_model.to_entity() if interaction_model else None

    async def update(self, interaction: Interaction):
        query = (
            update(InteractionModel)
            .where(InteractionModel.id == interaction.id)
            .values(
                first_user_id=interaction.first_user_id,
                second_user_id=interaction.second_user_id,
                first_user_interaction_type=interaction.first_user_interaction_type,
                second_user_interaction_type=interaction.second_user_interaction_type,
            )
        )
        await self.session.execute(query)
