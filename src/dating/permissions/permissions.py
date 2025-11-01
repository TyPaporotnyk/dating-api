from abc import ABC, abstractmethod

from dating.auth.entities import User


class Permission(ABC):
    @abstractmethod
    def __call__(self, user: User) -> bool: ...
