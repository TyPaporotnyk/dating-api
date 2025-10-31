from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    total: int
    page: int
    size: int


class Meta(BaseModel):
    pagination: Pagination | None = None


class MessageSchema(BaseModel):
    message: str


class ApiResponse(BaseModel, Generic[T]):
    data: T | None = None
    meta: Meta | None = None
