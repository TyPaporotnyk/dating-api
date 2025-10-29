import asyncio
import concurrent.futures
import functools
from dataclasses import dataclass
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from dating.photos.exceptions import ImageDeleteError, ImageUploadError
from dating.storages.base import Storage


@dataclass(frozen=True)
class S3Credentials:
    bucket_name: str
    public_url: str
    endpoint_url: str
    access_key_id: str
    secret_access_key: str


class S3Storage(Storage):
    def __init__(self, credentials: S3Credentials):
        self._bucket = credentials.bucket_name
        self._public_url = credentials.public_url
        self._client = boto3.client(
            "s3",
            endpoint_url=credentials.endpoint_url,
            aws_access_key_id=credentials.access_key_id,
            aws_secret_access_key=credentials.secret_access_key,
        )

        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

    async def _run_in_executor(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        bound_func = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(self._executor, bound_func)

    async def upload(self, file: bytes, path: str | Path, file_name: str) -> str:
        object_key = f"{path}/{file_name}".lstrip("/")

        try:
            await self._run_in_executor(
                self._client.put_object,
                Bucket=self._bucket,
                Key=object_key,
                Body=file,
                ContentType="image/jpeg",
                ACL="public-read",
            )
        except ClientError as e:
            raise ImageUploadError from e

        return object_key

    async def delete(self, path: str | Path):
        try:
            await self._run_in_executor(
                self._client.delete_object,
                Bucket=self._bucket,
                Key=path,
            )
        except ClientError as e:
            raise ImageDeleteError from e
