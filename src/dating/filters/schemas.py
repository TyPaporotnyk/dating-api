from pydantic import BaseModel

from dating.enums import Gender
from dating.filters.entities import ProfileFilter


class BaseProfileFilterSchema(BaseModel):
    gender_preference: Gender
    age_min: int = 18
    age_max: int = 99
    max_distance_meters: int = 10000
    show_only_with_photos: bool = False


class CreateProfileFilterSchema(BaseProfileFilterSchema): ...


class UpdateProfileFilterSchema(BaseProfileFilterSchema): ...


class ResponseProfileFilterSchema(BaseProfileFilterSchema):
    @classmethod
    def from_dto(cls, entity: ProfileFilter) -> "ResponseProfileFilterSchema":
        return cls(
            gender_preference=entity.gender_preference,
            age_min=entity.age_min,
            age_max=entity.age_max,
            max_distance_meters=entity.max_distance_meters,
            show_only_with_photos=entity.show_only_with_photos,
        )
