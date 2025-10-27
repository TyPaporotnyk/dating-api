from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class UserAlreadyExist(AppException):
    error_code: str = "USER_ALREDY_EXIST"

    @property
    def message(self) -> str:
        return "User already exist"


@dataclass(kw_only=True)
class UserNotFound(AppException):
    error_code: str = "USER_NOT_FOUND"

    @property
    def message(self) -> str:
        return "User not found"


@dataclass(kw_only=True)
class AuthError(AppException):
    error_code: str = "AUTH_ERROR"

    @property
    def message(self) -> str:
        return "Auth error"


@dataclass(kw_only=True)
class InvalidAccessToken(AppException):
    error_code = "INVALID_AUTH_TOKEN"

    @property
    def message(self) -> str:
        return "Invalid auth token"
