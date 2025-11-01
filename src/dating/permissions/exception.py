from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class AccessDenied(AppException):
    error_code: str = "ACCESS_DENIED"
