from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from dating.entities import Entity

T = TypeVar("T", bound=Entity)


@dataclass(kw_only=True)
class BasePool(ABC, Generic[T]):
    pool_obj_type: type[T]

    def _get_pool_key(self, key: str) -> str:
        return f"pool:{self.pool_obj_type.__name__}:{key}"

    @abstractmethod
    async def next_from_pool(self, key: str) -> T | None: ...

    @abstractmethod
    async def put_to_pool(self, key: str, obj: T | list[T], clear: bool = False): ...

    @abstractmethod
    async def get_pool_size(self, key: str) -> int: ...
