from fastapi import FastAPI, APIRouter
from starlette.responses import JSONResponse

from dating.users.routers import router as user_router


def setup(app: FastAPI):
    api_router = APIRouter(
        default_response_class=JSONResponse,
    )

    api_router.include_router(user_router, prefix="/users", tags=["users"])

    app.include_router(api_router, prefix="/api/v1")
