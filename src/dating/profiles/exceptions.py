from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class ProfileNotFound(AppException):
    error_code: str = "PROFILE_NOT_FOUND"
