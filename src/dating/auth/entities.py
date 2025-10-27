from dataclasses import dataclass
from passlib.context import CryptContext

from dating.entities import Entity
from dating.utils.jwt import gen_jwt_token

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


@dataclass
class User(Entity):
    email: str
    hashed_password: str | None = None

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def validate_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @property
    def token(self) -> str:
        return gen_jwt_token(user_id=self.id)
