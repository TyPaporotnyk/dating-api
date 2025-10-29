from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class ImageNotFound(AppException):
    error_code: str = "IMAGE_NOT_FOUND"


@dataclass(kw_only=True)
class ImageUploadError(AppException):
    error_code: str = "FAILED_UPLOAD_IMAGE"


@dataclass(kw_only=True)
class ImageDeleteError(AppException):
    error_code: str = "FAILED_DELETE_IMAGE"


@dataclass(kw_only=True)
class MaxProfileImagesCountReached(AppException):
    error_code: str = "MAX_PROFILE_IMAGES_COUNT_REACHED"
