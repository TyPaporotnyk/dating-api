from dataclasses import dataclass

from dating.exceptions import AppException


@dataclass(kw_only=True)
class EmailSendError(AppException):
    error_code: str = "EMAIL_SEND_ERROR"
