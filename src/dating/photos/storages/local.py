from pathlib import Path

import aiofiles
from aiofiles import os

from dating.photos.storages.base import Storage


class LocalStorage(Storage):
    async def upload(self, file: bytes, path: Path, file_name: str) -> str:
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / file_name

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file)

        return str(file_path)

    async def delete(self, path: Path):
        if path.exists():
            await os.remove(path)
