from uuid import UUID

from pydantic import BaseModel

from dating.enums import Gender
from dating.profiles.entities import Profile
from dating.value_objects import Coordinates


class BaseProfileSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: Gender


class CreateProfileSchema(BaseProfileSchema): ...


class UpdateProfileSchema(BaseProfileSchema): ...


class ResponseProfileSchema(BaseProfileSchema):
    id: UUID
    user_id: UUID
    location: Coordinates | None = None

    @classmethod
    def from_dto(cls, profile: Profile) -> "ResponseProfileSchema":
        return cls(
            id=profile.id,
            user_id=profile.user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            age=profile.age,
            gender=profile.gender,
            location=profile.location,
        )


class UpdateProfileLocationSchema(BaseModel):
    latitude: float
    longitude: float
