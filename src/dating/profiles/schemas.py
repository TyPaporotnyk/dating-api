from pydantic import BaseModel

from dating.profiles.entities import Profile
from dating.enums import Gender


class CreateProfileSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: Gender


class ResponseProfileSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: Gender

    @classmethod
    def from_dto(cls, profile: Profile) -> "ResponseProfileSchema":
        return cls(
            first_name=profile.first_name,
            last_name=profile.last_name,
            age=profile.age,
            gender=profile.gender,
        )
