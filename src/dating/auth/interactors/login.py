from dataclasses import dataclass

from dating.auth.commands import LoginUserCommand
from dating.auth.entities import User
from dating.auth.exceptions import AuthError
from dating.auth.repositories.base import BaseUserRepository


@dataclass
class LoginUserInteractor:
    user_repository: BaseUserRepository

    async def __call__(self, command: LoginUserCommand) -> User:
        user = await self.user_repository.get_by_email(email=command.email)
        if user and user.validate_password(password=command.password):
            return user

        raise AuthError
