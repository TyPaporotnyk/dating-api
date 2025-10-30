from pydantic import BaseModel, EmailStr

from dating.auth.entities import User
from dating.auth.services.jwt import TokenPair


class BaseUserSchema(BaseModel):
    email: EmailStr
    is_verified: bool


class ResponseUserSchema(BaseUserSchema):
    @classmethod
    def from_dto(cls, user: User) -> "ResponseUserSchema":
        return ResponseUserSchema(email=user.email, is_verified=user.is_verified)


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: float
    refresh_expires_in: float
    token_type: str = "bearer"

    @classmethod
    def from_dto(cls, entity: TokenPair) -> "TokenPairResponse":
        return cls(
            access_token=entity.access_token,
            refresh_token=entity.refresh_token,
            expires_in=entity.expires_in,
            refresh_expires_in=entity.refresh_expires_in,
        )


class VerificationUserSubmitSchema(BaseModel):
    code: str
