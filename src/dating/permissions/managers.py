from dating.auth.dependencies import CurrentUser
from dating.permissions.exception import AccessDenied
from dating.permissions.permissions import Permission


class FastApiPermissionManager:
    def __init__(self, permissions: tuple[Permission]):
        self.permissions = permissions

    def __call__(self, user: CurrentUser):
        for permission in self.permissions:
            if not permission(user):
                raise AccessDenied

    def __hash__(self) -> int:
        return hash(self.permissions)
