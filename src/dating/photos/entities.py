from dataclasses import dataclass
from uuid import UUID

from dating.entities import Entity


@dataclass
class ProfilePhoto(Entity):
    profile_id: UUID
    
    url: str
    order: int = 0
    is_main: bool = False
