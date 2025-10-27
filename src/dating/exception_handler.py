from typing import Type
from fastapi import Request, status
from fastapi.responses import JSONResponse

from dating.exceptions import AppException
from dating.auth.exceptions import UserNotFound, AuthError


def get_http_status_code(exc: Exception) -> int:
    exc_to_status: dict[Type[Exception], int] = {
        UserNotFound: status.HTTP_404_NOT_FOUND,
        AuthError: status.HTTP_403_FORBIDDEN,
    }
    return exc_to_status.get(type(exc), status.HTTP_400_BAD_REQUEST)


async def generate_exception_request(request: Request, exc: AppException) -> JSONResponse:
    status_code = get_http_status_code(exc)

    return JSONResponse(
        status_code=status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )
