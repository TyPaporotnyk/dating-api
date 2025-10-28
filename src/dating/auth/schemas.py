from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from dating.auth.entities import User
from dating.utils.datetime import get_datetime_utc_now
from dating.utils.uuid_v7 import uuid7


class BaseUserSchema(BaseModel):
    id: UUID = Field(default_factory=uuid7)
    created_at: datetime = Field(default_factory=get_datetime_utc_now)
    updated_at: datetime = Field(default_factory=get_datetime_utc_now)


class ResponseUserSchema(BaseUserSchema):
    email: EmailStr

    @classmethod
    def from_dto(cls, user: User) -> "ResponseUserSchema":
        return ResponseUserSchema(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(BaseModel):
    token: str

    @classmethod
    def from_dto(cls, user: User) -> "LoginUserResponse":
        return cls(token=user.token)
