import logging
from pathlib import Path

from starlette.config import Config

logger = logging.getLogger(__name__)
config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

JWT_SECRET = config("JWT_SECRET", default=None)
JWT_ALG = config("JWT_ALG", default="HS256")
JWT_ACCESS_EXP = config("JWT_ACCESS_EXP", cast=int, default=86400)
JWT_REFRESH_EXP = config("JWT_REFRESH_EXP", cast=int, default=2592000)

if not JWT_SECRET:
    logger.warning(
        "JWT secret not provided, this is required if you are using basic authentication"
    )

STATIC_DIR = BASE_DIR / "static"
STATIC_PATH = "/static"

MEDIA_DIR = BASE_DIR / "media"
MEDIA_PATH = "/media"

REDIS_HOST = config("REDIS_HOST", default="127.0.0.1")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_DB = config("REDIS_DB", cast=int, default=0)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

S3_ENDPOINT_URL = config("S3_ENDPOINT_URL")
S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = config("S3_BUCKET_NAME")
S3_PUBLIC_URL = config("S3_PUBLIC_URL")

RABBITMQ_HOST = config("RABBITMQ_HOST", default="127.0.0.1")
RABBITMQ_PORT = config("RABBITMQ_PORT", cast=int, default=5672)
RABBITMQ_USER = config("RABBITMQ_USER")
RABBITMQ_PASSWORD = config("RABBITMQ_PASSWORD")

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"

MATCH_NOTIFICATION_QUEUE = config("MATCH_NOTIFICATION_QUEUE", default="user_match_notification")

MAX_PROFILE_IMAGES = 6

CANDIDATES_GEN_SIZE = 50
CANDIDATEs_MIN_POOL_SIZE = 10

RESEND_API_KEY = config("RESEND_API_KEY")

NOTIFICATION_EMAIL_WORKER_EMAIL = config("NOTIFICATION_EMAIL_WORKER_EMAIL")

VERIFICATION_CODE_TTL = config("VERIFICATION_CODE_TTL", cast=int, default=600)
