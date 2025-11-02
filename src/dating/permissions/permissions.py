from abc import ABC, abstractmethod

from dating.auth.entities import User
from dating.permissions.exception import PermissionException


class Permission(ABC):
    exception_class: type[PermissionException]

    def __call__(self, user: User):
        if not self.validate(user):
            raise self.exception_class

    @abstractmethod
    def validate(self, user: User) -> bool: ...
