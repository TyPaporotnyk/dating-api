from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError, decode, encode
from pydantic import BaseModel, ValidationError
from redis.asyncio import Redis

from dating.auth.exceptions import InvalidRefreshToken, InvalidToken
from dating.config import JWT_ACCESS_EXP, JWT_ALG, JWT_REFRESH_EXP, JWT_SECRET


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int


class JWTPayload(BaseModel):
    jti: UUID
    iat: float
    exp: float
    sub: UUID
    type: str


@dataclass
class JWTService:
    redis: Redis

    def _encode(self, payload: JWTPayload) -> str:
        payload_data = {
            "jti": str(payload.jti),
            "iat": payload.iat,
            "exp": payload.exp,
            "sub": str(payload.sub),
            "type": payload.type,
        }
        return encode(payload_data, JWT_SECRET, algorithm=JWT_ALG)

    def _generate_payload(self, user_id: UUID, token_type: str, exp_seconds: int) -> JWTPayload:
        now = datetime.now(UTC)
        return JWTPayload(
            jti=uuid4(),
            iat=now.timestamp(),
            exp=(now + timedelta(seconds=exp_seconds)).timestamp(),
            sub=user_id,
            type=token_type,
        )

    def _decode(self, token: str) -> JWTPayload:
        try:
            payload = decode(token, JWT_SECRET, algorithms=[JWT_ALG])
            return JWTPayload.model_validate(payload)
        except ExpiredSignatureError as e:
            raise InvalidToken from e
        except DecodeError as e:
            raise InvalidToken from e
        except InvalidTokenError as e:
            raise InvalidToken from e
        except ValidationError as e:
            raise InvalidToken from e

    async def _check_revoked(self, jti: UUID) -> bool:
        return not await self.redis.exists(f"refresh:{jti}")

    async def _store_refresh(self, payload: JWTPayload):
        await self.redis.setex(f"refresh:{payload.jti}", JWT_REFRESH_EXP, str(payload.sub))

    async def generate_token_pair(self, user_id: UUID) -> TokenPair:
        access_payload = self._generate_payload(user_id, "access", JWT_ACCESS_EXP)
        refresh_payload = self._generate_payload(user_id, "refresh", JWT_REFRESH_EXP)

        await self._store_refresh(refresh_payload)

        return TokenPair(
            access_token=self._encode(access_payload),
            refresh_token=self._encode(refresh_payload),
            expires_in=JWT_ACCESS_EXP,
            refresh_expires_in=JWT_REFRESH_EXP,
        )

    async def validate_token(self, token: str) -> JWTPayload:
        payload = self._decode(token)
        if await self._check_revoked(payload.jti):
            raise InvalidToken
        return payload

    async def refresh_tokens(self, refresh_token: str) -> TokenPair:
        payload = self._decode(refresh_token)

        if payload.type != "refresh":
            raise InvalidRefreshToken

        if await self._check_revoked(payload.jti):
            raise InvalidRefreshToken

        await self.redis.delete(f"refresh:{payload.jti}")

        return await self.generate_token_pair(payload.sub)
