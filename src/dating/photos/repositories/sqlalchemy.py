from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from dating.photos.models import ProfilePhotoModel
from dating.photos.entities import ProfilePhoto
from dating.photos.repositories.base import BaseProfileImageRepository


class SQLAlchemyProfileImageRepository(BaseProfileImageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, profile_photo: ProfilePhoto) -> None:
        user_model = ProfilePhotoModel.from_entity(profile_photo)
        self.session.add(user_model)

    async def get_all(self, profile_id: UUID) -> list[ProfilePhoto]:
        result = await self.session.execute(
            select(ProfilePhotoModel)
            .where(ProfilePhotoModel.profile_id == profile_id)
            .order_by(ProfilePhotoModel.order.asc())
        )
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def delete(self, photo_id: UUID) -> None:
        await self.session.execute(
            delete(ProfilePhotoModel).where(ProfilePhotoModel.id == photo_id)
        )
