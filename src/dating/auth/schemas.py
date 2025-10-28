from pydantic import BaseModel, EmailStr

from dating.auth.entities import User


class BaseUserSchema(BaseModel):
    email: EmailStr


class ResponseUserSchema(BaseUserSchema):
    @classmethod
    def from_dto(cls, user: User) -> "ResponseUserSchema":
        return ResponseUserSchema(email=user.email)


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
