from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class ProfileNotFound(AppException):
    error_code: str = "PROFILE_NOT_FOUND"


@dataclass(kw_only=True)
class ProfileAlreadyExists(AppException):
    error_code: str = "PROFILE_ALREADY_EXISTS"


@dataclass(kw_only=True)
class ProfileLocationRequired(AppException):
    error_code: str = "PROFILE_LOCATION_REQUIRED"
