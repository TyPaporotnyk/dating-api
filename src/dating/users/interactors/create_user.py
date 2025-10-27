from dataclasses import dataclass

from dating.database.managers.base import TransactionManager
from dating.users.commands.create_user import CreateUserCommand
from dating.users.exceptions import UserAlreadyExist
from dating.users.repositories.base import BaseUserRepository
from dating.users.entities import User


@dataclass
class CreateUserInteractor:
    user_repository: BaseUserRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: CreateUserCommand) -> User:
        if await self.user_repository.get_by_email(email=command.email):
            raise UserAlreadyExist

        user = User(email=command.email)
        await self.user_repository.create(user)
        await self.transaction_manager.commit()
        return user
