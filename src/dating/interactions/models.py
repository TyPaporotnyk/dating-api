from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from dating.database.core import BaseModel
from dating.database.mixins import TimeStampMinix, UUIDMixin
from dating.enums import InteractionType
from dating.interactions.entities import Interaction


class InteractionModel(BaseModel, UUIDMixin, TimeStampMinix):
    __tablename__ = "user_interactions"

    first_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    second_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )

    first_user_interaction_type: Mapped[InteractionType] = mapped_column(
        ENUM(InteractionType, name="interaction_type_enum"), nullable=True
    )

    second_user_interaction_type: Mapped[InteractionType] = mapped_column(
        ENUM(InteractionType, name="interaction_type_enum"), nullable=True
    )

    @classmethod
    def from_entity(cls, entity: Interaction) -> "InteractionModel":
        return cls(
            id=entity.id,
            first_user_id=entity.first_user_id,
            second_user_id=entity.second_user_id,
            first_user_interaction_type=entity.first_user_interaction_type,
            second_user_interaction_type=entity.second_user_interaction_type,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> Interaction:
        return Interaction(
            id=self.id,
            first_user_id=self.first_user_id,
            second_user_id=self.second_user_id,
            first_user_interaction_type=self.first_user_interaction_type,
            second_user_interaction_type=self.second_user_interaction_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
