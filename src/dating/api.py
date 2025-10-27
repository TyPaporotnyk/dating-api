from fastapi import FastAPI, APIRouter

from dating.auth.routers import auth_router, user_router
from dating.profiles.routers import router as profile_router


def setup(app: FastAPI):
    api_router = APIRouter()

    api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

    account_router = APIRouter()

    account_router.include_router(profile_router, prefix="/profile", tags=["profile"])
    account_router.include_router(user_router, prefix="/me", tags=["user"])

    api_router.include_router(account_router, prefix="/users")

    app.include_router(api_router, prefix="/api/v1")
