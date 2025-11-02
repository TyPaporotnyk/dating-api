from collections.abc import AsyncGenerator

from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from dating import config


def create_db_engine(connection_string: str):
    url = make_url(connection_string)

    timeout_kwargs = {
        "future": True,
        "plugins": ["geoalchemy2"],
        "pool_timeout": config.DATABASE_ENGINE_POOL_TIMEOUT,
        "pool_recycle": config.DATABASE_ENGINE_POOL_RECYCLE,
        "pool_size": config.DATABASE_ENGINE_POOL_SIZE,
        "max_overflow": config.DATABASE_ENGINE_MAX_OVERFLOW,
        "pool_pre_ping": config.DATABASE_ENGINE_POOL_PING,
    }

    return create_async_engine(url, **timeout_kwargs)


engine = create_db_engine(
    config.SQLALCHEMY_DATABASE_URI,
)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


class BaseModel(DeclarativeBase):
    pass
