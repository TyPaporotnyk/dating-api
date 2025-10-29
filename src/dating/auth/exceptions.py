from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class UserAlreadyExist(AppException):
    error_code: str = "USER_ALREADY_EXIST"


@dataclass(kw_only=True)
class UserNotFound(AppException):
    error_code: str = "USER_NOT_FOUND"


@dataclass(kw_only=True)
class AuthError(AppException):
    error_code: str = "AUTH_ERROR"


@dataclass(kw_only=True)
class InvalidToken(AppException):
    error_code: str = "INVALID_TOKEN"


@dataclass(kw_only=True)
class InvalidAccessToken(InvalidToken):
    error_code: str = "INVALID_ACCESS_TOKEN"


@dataclass(kw_only=True)
class InvalidRefreshToken(InvalidToken):
    error_code: str = "INVALID_REFRESH_TOKEN"
