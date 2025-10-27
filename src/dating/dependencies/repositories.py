from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope, provide

from dating.users.repositories.base import BaseUserRepository
from dating.users.repositories.sqlalchemy import SQLAlchemyUserRepository


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session=session)
