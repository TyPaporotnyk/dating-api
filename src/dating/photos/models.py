from uuid import UUID
from sqlalchemy import ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column

from dating.database.core import BaseModel
from dating.database.mixins import UUIDMixin, TimeStampMinix
from dating.photos.entities import ProfilePhoto


class ProfilePhotoModel(BaseModel, UUIDMixin, TimeStampMinix):
    __tablename__ = "profile_photos"

    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(nullable=False)
    is_main: Mapped[bool] = mapped_column(default=False, server_default=false(), nullable=False)
    order: Mapped[int] = mapped_column(default=0, nullable=False, index=True)

    @classmethod
    def from_entity(cls, profile_photo: ProfilePhoto) -> "ProfilePhotoModel":
        return cls(
            id=profile_photo.id,
            profile_id=profile_photo.profile_id,
            url=profile_photo.url,
            is_main=profile_photo.is_main,
            order=profile_photo.order,
            created_at=profile_photo.created_at,
            updated_at=profile_photo.updated_at,
        )

    def to_entity(self) -> ProfilePhoto:
        return ProfilePhoto(
            id=self.id,
            profile_id=self.profile_id,
            url=self.url,
            is_main=self.is_main,
            order=self.order,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
