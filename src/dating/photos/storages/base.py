from pathlib import Path
from typing import Protocol


class Storage(Protocol):
    async def upload(self, file: bytes, path: str | Path, file_name: str) -> str: ...

    async def delete(self, path: str | Path) -> None: ...
