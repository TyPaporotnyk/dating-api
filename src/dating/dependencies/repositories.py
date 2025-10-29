from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from dating.auth.repositories.base import BaseUserRepository
from dating.auth.repositories.sqlalchemy import SQLAlchemyUserRepository
from dating.candidates.repositories.base import BaseCandidatesRepository
from dating.candidates.repositories.sqlalchemy import SQLAlchemyCandidatesRepository
from dating.filters.repositories.base import BaseProfileFilterRepository
from dating.filters.repositories.sqlalchemy import SQLAlchemyProfileFilterRepository
from dating.interactions.repositories.base import BaseInteractionRepository
from dating.interactions.repositories.sqlalchemy import SQLAlchemyInteractionRepository
from dating.photos.repositories.base import BaseProfileImageRepository
from dating.photos.repositories.sqlalchemy import SQLAlchemyProfileImageRepository
from dating.profiles.repositories.base import BaseProfileRepository
from dating.profiles.repositories.sqlalchemy import SQLAlchemyProfileRepository


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_profile_repository(self, session: AsyncSession) -> BaseProfileRepository:
        return SQLAlchemyProfileRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_profile_photo_repository(self, session: AsyncSession) -> BaseProfileImageRepository:
        return SQLAlchemyProfileImageRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_profile_filter_repository(self, session: AsyncSession) -> BaseProfileFilterRepository:
        return SQLAlchemyProfileFilterRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_candidates_repository(self, session: AsyncSession) -> BaseCandidatesRepository:
        return SQLAlchemyCandidatesRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_interaction_repository(self, session: AsyncSession) -> BaseInteractionRepository:
        return SQLAlchemyInteractionRepository(session=session)
