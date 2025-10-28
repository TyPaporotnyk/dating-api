from fastapi import APIRouter, FastAPI

from dating.auth.routers import auth_router, user_router
from dating.filters.routers import router as profile_filter_router
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

    api_router.include_router(account_router, prefix="/users")

    app.include_router(api_router, prefix="/api/v1")
