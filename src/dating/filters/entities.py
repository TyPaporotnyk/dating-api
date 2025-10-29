from dataclasses import dataclass
from uuid import UUID

from dating.entities import Entity
from dating.enums import Gender


@dataclass
class ProfileFilter(Entity):
    user_id: UUID

    gender_preference: Gender
    age_min: int = 18
    age_max: int = 99
    max_distance_meters: int = 10000
    show_only_with_photos: bool = False
