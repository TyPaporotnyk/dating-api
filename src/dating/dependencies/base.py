from collections.abc import AsyncGenerator

from aio_pika import connect_robust as rabbit_connect
from aio_pika.abc import AbstractRobustConnection
from dishka import Provider, Scope, provide
from httpx import AsyncClient
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncSession

from dating.candidates.commands import GetNextCandidateCommand
from dating.candidates.events import GenerateCandidatesPoolEvent
from dating.candidates.handlers.generate_candidates import GenerateCandidatesPoolEventHandler
from dating.candidates.handlers.get_candidates import GetNextCandidateCommandHandler
from dating.candidates.pools import CandidatePool
from dating.candidates.repositories.base import BaseCandidatesRepository
from dating.config import (
    RABBITMQ_URL,
    REDIS_URL,
    RESEND_API_KEY,
    S3_ACCESS_KEY_ID,
    S3_BUCKET_NAME,
    S3_ENDPOINT_URL,
    S3_PUBLIC_URL,
    S3_SECRET_ACCESS_KEY,
)
from dating.database.core import get_session
from dating.database.managers.base import TransactionManager
from dating.database.managers.sqlalchemy import SQLAlchemyTransactionManager
from dating.filters.repositories.base import BaseProfileFilterRepository
from dating.mediator.mediator import Mediator
from dating.notifications.clients.email.base import EmailClient
from dating.notifications.clients.email.resend import ResendEmailClient
from dating.profiles.repositories.base import BaseProfileRepository
from dating.storages.base import Storage
from dating.storages.s3 import S3Credentials, S3Storage


class BaseAppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async for session in get_session():
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

    @provide(scope=Scope.APP)
    async def get_email_client(self) -> AsyncGenerator[EmailClient]:
        async with AsyncClient(base_url="https://api.resend.com", timeout=30) as client:
            yield ResendEmailClient(http_client=client, api_key=RESEND_API_KEY)

    @provide(scope=Scope.APP)
    async def get_rabbit_connection(self) -> AbstractRobustConnection:
        return await rabbit_connect(RABBITMQ_URL)

    @provide(scope=Scope.REQUEST)
    async def get_mediator(
        self,
        profile_repository: BaseProfileRepository,
        profile_filter_repository: BaseProfileFilterRepository,
        candidates_repository: BaseCandidatesRepository,
        candidate_pool: CandidatePool,
    ) -> Mediator:
        mediator = Mediator()

        # Privede handlers
        get_next_candidate_handler = GetNextCandidateCommandHandler(
            _mediator=mediator, candidate_pool=candidate_pool
        )

        gen_candidates_handler = GenerateCandidatesPoolEventHandler(
            profile_repository=profile_repository,
            profile_filter_repository=profile_filter_repository,
            candidates_repository=candidates_repository,
            candidate_pool=candidate_pool,
        )

        # Register commands
        mediator.register_command(GetNextCandidateCommand, get_next_candidate_handler)

        # Register events
        mediator.register_events(GenerateCandidatesPoolEvent, [gen_candidates_handler])

        return mediator
