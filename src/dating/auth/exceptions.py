from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class UserAlreadyExist(AppException):
    error_code: str = "USER_ALREDY_EXIST"


@dataclass(kw_only=True)
class UserNotFound(AppException):
    error_code: str = "USER_NOT_FOUND"


@dataclass(kw_only=True)
class AuthError(AppException):
    error_code: str = "AUTH_ERROR"


@dataclass(kw_only=True)
class InvalidAccessToken(AppException):
    error_code = "INVALID_AUTH_TOKEN"
