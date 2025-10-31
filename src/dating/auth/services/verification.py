import random
import string
from dataclasses import dataclass

from redis.asyncio import Redis

from dating.config import VERIFICATION_CODE_TTL


@dataclass
class VerificationService:
    redis: Redis

    def _gen_code(self, length: int = 6) -> str:
        return "".join(random.choices(string.digits, k=length))

    def _get_storage_key(self, key: str) -> str:
        return f"verify:{key}"

    async def generate_and_save(self, target: str) -> str:
        code = self._gen_code()
        key = self._get_storage_key(target)
        await self.redis.set(key, code, ex=VERIFICATION_CODE_TTL)
        return code

    async def verify_code(self, target: str, code: str) -> bool:
        key = self._get_storage_key(target)
        stored_code = await self.redis.get(key)

        if stored_code is None:
            return False

        stored_code = stored_code.decode() if isinstance(stored_code, bytes) else stored_code
        if stored_code != code:
            return False

        await self.redis.delete(key)
        return True
