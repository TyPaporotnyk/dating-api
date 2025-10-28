from pathlib import Path
from typing import Union
from urllib.parse import urljoin

import aiofiles
from aiofiles import os

from dating.config import MEDIA_DIR, MEDIA_PATH
from dating.photos.storages.base import Storage


class LocalStorage(Storage):
    async def upload(self, file: bytes, path: Union[str, Path], file_name: str) -> str:
        path = Path(path)
        media_path = MEDIA_DIR / path
        media_path.mkdir(parents=True, exist_ok=True)

        file_path = media_path / file_name

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file)

        relative_path = path / file_name
        file_url = f"{MEDIA_PATH.rstrip('/')}/{relative_path.as_posix()}"

        return file_url

    async def delete(self, path: Path):
        if path.exists():
            await os.remove(path)
