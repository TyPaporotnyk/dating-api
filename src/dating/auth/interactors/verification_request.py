import logging
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from dating.auth.exceptions import AlreadyVerified
from dating.auth.repositories.base import BaseUserRepository
from dating.auth.services.verification import VerificationService
from dating.notifications.workers.email import EmailWorker

logger = logging.getLogger(__name__)


@dataclass
class VerificationRequestInteractor:
    user_repository: BaseUserRepository
    verification_service: VerificationService
    email_worker: EmailWorker

    async def __call__(self, user_id: UUID) -> Any:
        user = await self.user_repository.try_get_by_id(user_id=user_id)
        if user.is_verified:
            raise AlreadyVerified

        verification_code = await self.verification_service.generate_and_save(target=user.email)
        await self.email_worker.send_verification(recipient=user.email, code=verification_code)
        logger.info("Verification code sent: %s", user.email)
