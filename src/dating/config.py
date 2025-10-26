import logging

from pathlib import Path
from starlette.config import Config

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")

BASE_DIR = Path(__file__).resolve().parent

DATABASE_NAME = config("DATABASE_NAME")
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT")

DATABASE_ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=10)
DATABASE_ENGINE_POOL_PING = config("DATABASE_ENGINE_POOL_PING", default=False)
DATABASE_ENGINE_POOL_RECYCLE = config("DATABASE_ENGINE_POOL_RECYCLE", cast=int, default=3600)
DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
DATABASE_ENGINE_POOL_TIMEOUT = config("DATABASE_ENGINE_POOL_TIMEOUT", cast=int, default=30)
SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
