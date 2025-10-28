from datetime import UTC, datetime, timedelta
from uuid import UUID

from jwt import decode, encode, exceptions

from dating.auth.exceptions import InvalidAccessToken
from dating.config import JWT_ALG, JWT_EXP, JWT_SECRET


def gen_jwt_token(user_id: UUID) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
    data = {
        "exp": exp,
        "user_id": str(user_id),
    }
    return encode(data, JWT_SECRET, algorithm=JWT_ALG)


def validate_jwt_token(token: str) -> UUID | None:
    try:
        payload = decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except exceptions.DecodeError as e:
        raise InvalidAccessToken from e
    except exceptions.ExpiredSignatureError as e:
        raise InvalidAccessToken from e

    user_id = payload.get("user_id")
    return UUID(user_id) if user_id else None
