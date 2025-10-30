import json
from dataclasses import dataclass

from redis.asyncio import Redis

from dating.pools.base import BasePool, T


@dataclass(kw_only=True)
class RedisPool(BasePool[T]):
    redis: Redis

    async def next_from_pool(self, key: str) -> T | None:
        pool_key = self._get_pool_key(key)
        obj_str: str | None = await self.redis.lpop(pool_key)  # type: ignore
        if not obj_str:
            return None

        obj_data = json.loads(obj_str)
        return self.pool_obj_type.from_dict(obj_data)

    async def put_to_pool(self, key: str, obj: T | list[T], clear: bool = False):
        pool_key = self._get_pool_key(key)
        pipe = self.redis.pipeline()
        if clear:
            pipe.delete(pool_key)

        objs = obj if isinstance(obj, list) else [obj]
        for obj in objs:
            pipe.rpush(pool_key, json.dumps(obj.to_dict(), default=str))

        await pipe.execute()

    async def get_pool_size(self, key: str) -> int:
        pool_key = self._get_pool_key(key)
        return await self.redis.llen(pool_key) or 0  # type: ignore
