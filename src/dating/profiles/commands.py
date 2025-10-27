from dataclasses import dataclass
from uuid import UUID

from dating.commands import BaseCommand
from dating.enums import Gender


@dataclass(frozen=True)
class CreateProfileCommand(BaseCommand):
    first_name: str
    last_name: str
    age: int
    gender: Gender

    user_id: UUID
