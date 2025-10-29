from uuid import UUID

from geoalchemy2 import Geography, WKBElement
from geoalchemy2.shape import to_shape
from shapely import Point as SH_Point
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from dating.database.core import BaseModel
from dating.database.mixins import TimeStampMinix, UUIDMixin
from dating.enums import Gender
from dating.profiles.entities import Profile
from dating.value_objects.coordinates import Coordinates


class ProfileModel(BaseModel, UUIDMixin, TimeStampMinix):
    __tablename__ = "profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[Gender] = mapped_column(ENUM(Gender, name="gender_enum"), nullable=False)

    location: Mapped[WKBElement] = mapped_column(
        Geography("POINT", srid=4326),
        nullable=True,
    )

    @classmethod
    def from_entity(cls, entity: Profile) -> "ProfileModel":
        return cls(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            age=entity.age,
            gender=entity.gender,
            user_id=entity.user_id,
            location=entity.location,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> Profile:
        coordinates = None
        if self.location:
            sh_point = to_shape(self.location)
            if isinstance(sh_point, SH_Point):
                coordinates = Coordinates(latitude=sh_point.y, longitude=sh_point.x)

        return Profile(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            age=self.age,
            gender=self.gender,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            location=coordinates,
        )
