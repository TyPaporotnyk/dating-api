from dataclasses import dataclass
from uuid import UUID

from dating.entities import Entity
from dating.profiles.enums import Gender


@dataclass
class Profile(Entity):
    first_name: str
    last_name: str
    age: int
    gender: Gender
    user_id: UUID
