from dataclasses import dataclass

from dating.auth.commands import LoginUserCommand
from dating.auth.exceptions import AuthError
from dating.auth.repositories.base import BaseUserRepository
from dating.auth.services.jwt import JWTService, TokenPair


@dataclass
class LoginUserInteractor:
    user_repository: BaseUserRepository
    token_service: JWTService

    async def __call__(self, command: LoginUserCommand) -> TokenPair:
        user = await self.user_repository.get_by_email(email=command.email)
        if user and user.validate_password(password=command.password):
            token_pair = await self.token_service.generate_token_pair(user_id=user.id)
            return token_pair

        raise AuthError
