from dataclasses import dataclass
from uuid import UUID

from dating.config import S3_PUBLIC_URL
from dating.entities import Entity


@dataclass
class ProfilePhoto(Entity):
    profile_id: UUID

    url: str
    order: int = 0
    is_main: bool = False

    @property
    def full_url(self) -> str:
        return f"{S3_PUBLIC_URL}/{self.url}"
