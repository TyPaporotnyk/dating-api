from dataclasses import dataclass

from dating.commands import BaseCommand
from dating.enums import Gender


@dataclass(frozen=True)
class CreateProfileFilterCommand(BaseCommand):
    gender_preference: Gender
    age_min: int = 18
    age_max: int = 99
    max_distance_meters: int = 10000
    show_only_with_photos: bool = False


@dataclass(frozen=True)
class UpdateProfileFilterCommand(BaseCommand):
    gender_preference: Gender
    age_min: int
    age_max: int
    max_distance_meters: int
    show_only_with_photos: bool
