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


@dataclass(frozen=True)
class UpdateProfileCommand(BaseCommand):
    first_name: str
    last_name: str
    age: int
    gender: Gender
