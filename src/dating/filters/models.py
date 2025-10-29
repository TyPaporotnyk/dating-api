from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from dating.database.core import BaseModel
from dating.database.mixins import TimeStampMinix, UUIDMixin
from dating.enums import Gender
from dating.filters.entities import ProfileFilter


class ProfileFilterModel(BaseModel, UUIDMixin, TimeStampMinix):
    __tablename__ = "profile_filters"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    gender_preference: Mapped[Gender]
    age_min: Mapped[int] = mapped_column(default=18)
    age_max: Mapped[int] = mapped_column(default=99)
    max_distance_meters: Mapped[int] = mapped_column(default=10000)
    show_only_with_photos: Mapped[bool] = mapped_column(default=False)

    @classmethod
    def from_entity(cls, entity: ProfileFilter) -> "ProfileFilterModel":
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            gender_preference=entity.gender_preference,
            age_min=entity.age_min,
            age_max=entity.age_max,
            max_distance_meters=entity.max_distance_meters,
            show_only_with_photos=entity.show_only_with_photos,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> ProfileFilter:
        return ProfileFilter(
            id=self.id,
            user_id=self.user_id,
            gender_preference=self.gender_preference,
            age_min=self.age_min,
            age_max=self.age_max,
            max_distance_meters=self.max_distance_meters,
            show_only_with_photos=self.show_only_with_photos,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
