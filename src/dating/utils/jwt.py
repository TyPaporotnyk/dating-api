from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from dating.auth.exceptions import InvalidAccessToken
from dating.config import JWT_ALG, JWT_EXP, JWT_SECRET


def gen_jwt_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
    data = {
        "exp": exp,
        "user_id": str(user_id),
    }
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)


def validate_jwt_token(token: str) -> UUID | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.exceptions.DecodeError:
        raise InvalidAccessToken
    except jwt.ExpiredSignatureError:
        raise InvalidAccessToken()

    user_id = payload.get("user_id")
    return UUID(user_id) if user_id else None
