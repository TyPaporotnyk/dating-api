from dating.auth.entities import User
from dating.permissions.permissions import Permission


class IsVerified(Permission):
    def __call__(self, user: User) -> bool:
        return user.is_verified is True
