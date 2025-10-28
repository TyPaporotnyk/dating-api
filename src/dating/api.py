from fastapi import APIRouter, FastAPI

from dating.auth.routers import auth_router, user_router
from dating.photos.routers import router as photo_router
from dating.profiles.routers import router as profile_router


def setup(app: FastAPI) -> None:
    api_router = APIRouter()

    api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

    account_router = APIRouter()

    account_router.include_router(user_router, prefix="/me", tags=["user"])

    profile_router.include_router(photo_router, prefix="/photos", tags=["photos"])

    account_router.include_router(profile_router, prefix="/profile", tags=["profile"])

    api_router.include_router(account_router, prefix="/users")

    app.include_router(api_router, prefix="/api/v1")
