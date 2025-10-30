from fastapi import APIRouter, FastAPI

from dating.auth.routers import auth_router, user_router
from dating.candidates.routers import dev_router as candidates_dev_router
from dating.candidates.routers import router as candidate_router
from dating.config import ENV
from dating.filters.routers import router as profile_filter_router
from dating.interactions.routers import router as interaction_router
from dating.photos.routers import router as photo_router
from dating.profiles.routers import router as profile_router


def setup(app: FastAPI) -> None:
    api_router = APIRouter()

    api_router.include_router(auth_router, prefix="/auth")

    account_router = APIRouter()

    account_router.include_router(user_router, prefix="/me")

    account_router.include_router(profile_router, prefix="/profiles")
    account_router.include_router(photo_router, prefix="/photos")
    account_router.include_router(profile_filter_router, prefix="/filters")

    account_router.include_router(candidate_router, prefix="/candidates")

    if ENV.lower() in ["local", "dev"]:
        account_router.include_router(candidates_dev_router, prefix="/candidates")

    account_router.include_router(interaction_router)

    api_router.include_router(account_router, prefix="/users")

    app.include_router(api_router, prefix="/api/v1")
