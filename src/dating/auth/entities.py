from dataclasses import dataclass

from dating.entities import Entity
from dating.utils.jwt import gen_jwt_token
from dating.utils.pwd import pwd_service


@dataclass
class User(Entity):
    email: str
    hashed_password: str | None = None

    def set_password(self, password: str) -> None:
        self.hashed_password = pwd_service.hash_password(password)

    def validate_password(self, password: str) -> bool:
        if not self.hashed_password:
            raise ValueError("Password is not set")

        return pwd_service.validate_password(password, self.hashed_password)

    @property
    def token(self) -> str:
        return gen_jwt_token(user_id=self.id)
