import logging
from fastapi import FastAPI

from dating.logging import configure_logging
from dating.api import api_router

logger = logging.getLogger(__name__)
configure_logging()

app = FastAPI()

api = FastAPI(title="Dating api", description="Dating api", docs_url="/docs")

api.include_router(api_router)

app.mount("/api/v1", app=api)
