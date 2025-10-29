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

    async def get_interaction(self, from_user_id: UUID, to_user_id: UUID) -> Interaction | None:
        query = select(InteractionModel).where(
            and_(
                InteractionModel.from_user_id == from_user_id,
                InteractionModel.to_user_id == to_user_id,
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
                from_user_id=interaction.from_user_id,
                to_user_id=interaction.to_user_id,
                interaction_type=interaction.interaction_type,
                is_match=interaction.is_match,
            )
        )
        await self.session.execute(query)
