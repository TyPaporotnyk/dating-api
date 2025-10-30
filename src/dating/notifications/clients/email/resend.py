from dataclasses import dataclass

from httpx import AsyncClient, HTTPStatusError

from dating.notifications.clients.email.base import EmailClient
from dating.notifications.exceptions.clients import EmailSendError


@dataclass(frozen=True)
class ResendEmailClient(EmailClient):
    http_client: AsyncClient
    api_key: str

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def send(self, from_email: str, to_email: str, subject: str, html: str):
        json_data = {
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "html": html,
        }

        response = await self.http_client.post("/emails", json=json_data, headers=self.headers)

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            raise EmailSendError from e
