from pathlib import Path
from typing import Protocol, Union


class Storage(Protocol):
    async def upload(self, file: bytes, path: Union[str, Path], file_name: str) -> str:
        ...

    async def delete(self, path: Path):
        ...
