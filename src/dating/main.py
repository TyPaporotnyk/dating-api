import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from dating.dependencies.container import container
from dating.exception_handler import generate_exception_request
from dating.exceptions import AppException
from dating.logging import configure_logging
from dating import api

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

app.add_exception_handler(AppException, generate_exception_request)  # type: ignore

setup_dishka(container=container, app=app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api.setup(app)
