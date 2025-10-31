from sqlalchemy import Boolean, false
from sqlalchemy.orm import Mapped, mapped_column

from dating.auth.entities import User
from dating.database.core import BaseModel
from dating.database.mixins import TimeStampMinix, UUIDMixin


class UserModel(BaseModel, UUIDMixin, TimeStampMinix):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    hashed_password: Mapped[str] = mapped_column(nullable=False)

    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false(), nullable=False
    )

    @classmethod
    def from_entity(cls, entity: User) -> "UserModel":
        return cls(
            id=entity.id,
            email=entity.email,
            is_verified=entity.is_verified,
            hashed_password=entity.hashed_password,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            is_verified=self.is_verified,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
