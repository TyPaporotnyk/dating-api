from uuid import UUID

from sqlalchemy import ForeignKey, false
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from dating.database.core import BaseModel
from dating.database.mixins import TimeStampMinix, UUIDMixin
from dating.enums import InteractionType
from dating.interactions.entities import Interaction


class InteractionModel(BaseModel, UUIDMixin, TimeStampMinix):
    __tablename__ = "user_interactions"

    from_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    to_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    interaction_type: Mapped[InteractionType] = mapped_column(
        ENUM(InteractionType, name="interaction_type_enum"), nullable=False
    )

    is_match: Mapped[bool] = mapped_column(default=False, server_default=false(), nullable=False)

    @classmethod
    def from_entity(cls, entity: Interaction) -> "InteractionModel":
        return cls(
            id=entity.id,
            from_user_id=entity.from_user_id,
            to_user_id=entity.to_user_id,
            interaction_type=entity.interaction_type,
            is_match=entity.is_match,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> Interaction:
        return Interaction(
            id=self.id,
            from_user_id=self.from_user_id,
            to_user_id=self.to_user_id,
            interaction_type=self.interaction_type,
            is_match=self.is_match,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
