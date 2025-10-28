from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from dating.photos.entities import ProfilePhoto
from dating.photos.models import ProfilePhotoModel
from dating.photos.repositories.base import BaseProfileImageRepository


class SQLAlchemyProfileImageRepository(BaseProfileImageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, profile_photo: ProfilePhoto) -> None:
        user_model = ProfilePhotoModel.from_entity(profile_photo)
        self.session.add(user_model)

    async def get_by_profile_id_and_image_id(
        self, profile_id: UUID, image_id: UUID
    ) -> ProfilePhoto | None:
        query = select(ProfilePhotoModel).where(
            and_(
                ProfilePhotoModel.profile_id == profile_id,
                ProfilePhotoModel.id == image_id,
            )
        )
        result = await self.session.execute(query)
        image_model = result.scalar_one_or_none()
        return image_model.to_entity() if image_model else None

    async def get_all(self, profile_id: UUID) -> list[ProfilePhoto]:
        query = (
            select(ProfilePhotoModel)
            .where(ProfilePhotoModel.profile_id == profile_id)
            .order_by(ProfilePhotoModel.order.asc())
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def delete(self, image_id: UUID) -> None:
        await self.session.execute(
            delete(ProfilePhotoModel).where(ProfilePhotoModel.id == image_id)
        )
