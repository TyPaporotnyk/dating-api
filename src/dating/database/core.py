from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine.url import make_url

from dating import config


def create_db_engine(connection_string: str):
    url = make_url(connection_string)

    timeout_kwargs = {
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

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
