from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from dating.photos.entities import ProfilePhoto


class BaseProfilePhotoSchema(BaseModel):
    id: UUID

    url: str
    order: int = 0
    is_main: bool = False

    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, profile_photo: ProfilePhoto) -> "BaseProfilePhotoSchema":
        return cls(
            id=profile_photo.id,
            url=profile_photo.full_url,
            order=profile_photo.order,
            is_main=profile_photo.is_main,
            created_at=profile_photo.created_at,
            updated_at=profile_photo.updated_at,
        )
