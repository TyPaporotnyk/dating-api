from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class ImageNotFound(AppException):
    error_code: str = "IMAGE_NOT_FOUND"
