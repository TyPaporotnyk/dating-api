from abc import ABC, abstractmethod

from dating.auth.entities import User


class Permission(ABC):
    @abstractmethod
    async def has_permission(self, user: User) -> bool: ...


class And(Permission):
    def __init__(self, *perms: Permission):
        self.perms = perms

    async def has_permission(self, user: User) -> bool:
        return all([await p.has_permission(user) for p in self.perms])


class Or(Permission):
    def __init__(self, *perms: Permission):
        self.perms = perms

    async def has_permission(self, user: User) -> bool:
        return any([await p.has_permission(user) for p in self.perms])


class IsVerified(Permission):
    async def has_permission(self, user: User) -> bool:
        return user.is_verified
