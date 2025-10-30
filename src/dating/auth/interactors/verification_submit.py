import logging
from dataclasses import dataclass
from uuid import UUID

from dating.auth.exceptions import AlreadyVerified
from dating.auth.repositories.base import BaseUserRepository
from dating.auth.services.verification import VerificationService
from dating.database.managers.base import TransactionManager

logger = logging.getLogger(__name__)


@dataclass
class VerificationSubmitInteractor:
    user_repository: BaseUserRepository
    verification_service: VerificationService
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID, code: str) -> bool:
        user = await self.user_repository.try_get_by_id(user_id=user_id)
        if user.is_verified:
            raise AlreadyVerified

        if verified := await self.verification_service.verify_code(target=user.email, code=code):
            user.verify()
            await self.user_repository.update(user)
            await self.transaction_manager.commit()
            logger.info("User verified: %s", user.email)

        return verified
