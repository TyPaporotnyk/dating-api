from dataclasses import dataclass

from dating.config import NOTIFICATION_EMAIL_WORKER_EMAIL
from dating.notifications.clients.email.base import EmailClient
from dating.notifications.templates.email import get_verification_email_html
from dating.notifications.workers.base import NotificationWorker


@dataclass(kw_only=True)
class EmailWorker(NotificationWorker):
    email_client: EmailClient

    async def send_verification(self, recipient: str, code: str):
        html = get_verification_email_html(code=code)
        await self.email_client.send(
            NOTIFICATION_EMAIL_WORKER_EMAIL, to_email=recipient, subject="Verification", html=html
        )
