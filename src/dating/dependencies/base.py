from typing import AsyncGenerator
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from dating.database.core import async_session_maker
from dating.database.managers.base import TransactionManager
from dating.database.managers.sqlalchemy import SQLAlchemyTransactionManager


class BaseAppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_transaction_manager(self, session: AsyncSession) -> TransactionManager:
        return SQLAlchemyTransactionManager(session=session)
