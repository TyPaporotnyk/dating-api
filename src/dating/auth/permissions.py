from dating.auth.entities import User
from dating.auth.exceptions import NotVerified
from dating.permissions.permissions import Permission


class IsVerified(Permission):
    exception_class = NotVerified

    def validate(self, user: User) -> bool:
        return user.is_verified
