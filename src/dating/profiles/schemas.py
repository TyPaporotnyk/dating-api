from pydantic import BaseModel

from dating.enums import Gender
from dating.profiles.entities import Profile


class BaseProfileSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: Gender


class CreateProfileSchema(BaseProfileSchema): ...


class UpdateProfileSchema(BaseProfileSchema): ...


class ResponseProfileSchema(BaseProfileSchema):
    @classmethod
    def from_dto(cls, profile: Profile) -> "ResponseProfileSchema":
        return cls(
            first_name=profile.first_name,
            last_name=profile.last_name,
            age=profile.age,
            gender=profile.gender,
        )
