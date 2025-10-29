from dataclasses import dataclass

from dating.commands import BaseCommand


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserCommand(BaseCommand):
    email: str
    password: str
