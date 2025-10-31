from fastapi import Depends, HTTPException, status

from dating.auth.dependencies import get_current_user
from dating.auth.entities import User
from dating.permissions.permissions import Permission


async def require_permission(permission: Permission, user: User = Depends(get_current_user)):
    if not await permission.has_permission(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return user
