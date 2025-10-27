from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope, provide

from dating.auth.repositories.base import BaseUserRepository
from dating.auth.repositories.sqlalchemy import SQLAlchemyUserRepository


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session=session)
