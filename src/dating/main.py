import logging

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware
from slowapi.util import get_remote_address

from dating import api
from dating.config import REDIS_URL, STATIC_DIR, STATIC_PATH
from dating.dependencies.container import container
from dating.exception_handler import generate_exception_request
from dating.exceptions import AppException
from dating.logging import configure_logging

logger = logging.getLogger(__name__)
configure_logging()

swagger_ui_parameters = {
    "persistAuthorization": True,
    "displayRequestDuration": True,
    "tryItOutEnabled": True,
}

app = FastAPI(
    title="Dating api",
    description="Dating api",
    docs_url="/docs",
    swagger_ui_parameters=swagger_ui_parameters,
)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL,
    in_memory_fallback_enabled=True,
    strategy="moving-window",
    headers_enabled=True,
    default_limits=["100/minute"],
)

app.state.limiter = limiter
app.add_exception_handler(AppException, generate_exception_request)  # type: ignore
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

setup_dishka(container=container, app=app)

app.add_middleware(SlowAPIASGIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(STATIC_PATH, StaticFiles(directory=STATIC_DIR), name="static")

api.setup(app)
