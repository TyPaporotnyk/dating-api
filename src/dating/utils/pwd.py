from passlib.context import CryptContext


class PasswordService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def validate_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)


pwd_service = PasswordService()
