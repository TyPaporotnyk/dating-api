from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class FilterNotFound(AppException):
    error_code: str = "FILTER_NOT_FOUND"


@dataclass(kw_only=True)
class ProfileFilterAlreadyExists(AppException):
    error_code: str = "PROFILE_FILTER_ALREADY_EXISTS"
