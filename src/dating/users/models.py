from sqlalchemy.orm import Mapped, mapped_column

from dating.database.mixins import UUIDMixin, TimeStampMinix
from dating.database.core import BaseModel
from dating.users.entities import User


class UserModel(BaseModel, UUIDMixin, TimeStampMinix):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    @classmethod
    def from_entity(cls, entity: User) -> "UserModel":
        return cls(
            id=entity.id,
            email=entity.email,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id, email=self.email, created_at=self.created_at, updated_at=self.updated_at
        )
