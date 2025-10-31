from typing import Protocol


class NotificationWorker(Protocol):
    async def send_verification(self, recipient: str, code: str): ...
