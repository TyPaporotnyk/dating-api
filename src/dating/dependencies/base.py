from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncSession

from dating.config import (
    REDIS_URL,
    S3_ACCESS_KEY_ID,
    S3_BUCKET_NAME,
    S3_ENDPOINT_URL,
    S3_PUBLIC_URL,
    S3_SECRET_ACCESS_KEY,
)
from dating.database.core import async_session_maker
from dating.database.managers.base import TransactionManager
from dating.database.managers.sqlalchemy import SQLAlchemyTransactionManager
from dating.storages.base import Storage
from dating.storages.s3 import S3Credentials, S3Storage


class BaseAppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_transaction_manager(self, session: AsyncSession) -> TransactionManager:
        return SQLAlchemyTransactionManager(session=session)

    @provide(scope=Scope.APP)
    def get_storage_manager(self) -> Storage:
        return S3Storage(
            S3Credentials(
                bucket_name=S3_BUCKET_NAME,
                public_url=S3_PUBLIC_URL,
                endpoint_url=S3_ENDPOINT_URL,
                access_key_id=S3_ACCESS_KEY_ID,
                secret_access_key=S3_SECRET_ACCESS_KEY,
            )
        )

    @provide(scope=Scope.APP)
    def get_redis_client(self) -> Redis:
        return from_url(REDIS_URL)
