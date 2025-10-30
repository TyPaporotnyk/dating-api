from typing import Protocol


class EmailClient(Protocol):
    async def send(self, from_email: str, to_email: str, subject: str, html: str): ...
