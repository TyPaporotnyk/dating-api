from abc import ABC
from datetime import datetime
from uuid import UUID

from dataclasses import dataclass, field

from dating.utils.datetime import get_datetime_utc_now
from dating.utils.uuid_v7 import uuid7


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid7)
    created_at: datetime = field(default_factory=get_datetime_utc_now)
    updated_at: datetime = field(default_factory=get_datetime_utc_now)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
