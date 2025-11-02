from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class PermissionException(AppException):
    error_code: str = "PERMISSION_DENIED"
