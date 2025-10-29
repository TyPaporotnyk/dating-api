from dataclasses import dataclass

from dating.auth.commands import CreateUserCommand
from dating.auth.entities import User
from dating.auth.exceptions import UserAlreadyExist
from dating.auth.repositories.base import BaseUserRepository
from dating.database.managers.base import TransactionManager


@dataclass
class CreateUserInteractor:
    user_repository: BaseUserRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: CreateUserCommand) -> User:
        if await self.user_repository.get_by_email(email=command.email):
            raise UserAlreadyExist

        user = User(email=command.email)
        user.set_password(password=command.password)

        await self.user_repository.create(user)
        await self.transaction_manager.commit()
        return user
