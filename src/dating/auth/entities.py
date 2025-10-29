from dataclasses import dataclass

from dating.auth.services.pwd import pwd_service
from dating.entities import Entity


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
