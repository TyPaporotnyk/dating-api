from dataclasses import dataclass
from uuid import UUID

from dating.entities import Entity
from dating.enums import Gender
from dating.value_objects.coordinates import Coordinates


@dataclass
class Profile(Entity):
    first_name: str
    last_name: str
    age: int
    gender: Gender
    user_id: UUID

    location: Coordinates | None = None

    def update_location(self, coordinates: Coordinates) -> None:
        self.location = coordinates
