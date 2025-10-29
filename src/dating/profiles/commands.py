from dataclasses import dataclass

from dating.commands import BaseCommand
from dating.enums import Gender
from dating.value_objects.coordinates import Coordinates


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


@dataclass(frozen=True)
class UpdateProfileLocationCommand(BaseCommand):
    location: Coordinates
