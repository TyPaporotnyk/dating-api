from dataclasses import dataclass

from dating.commands import BaseCommand


@dataclass(frozen=True)
class CreateProfilePhotoCommand(BaseCommand):
    file: bytes
