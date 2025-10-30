from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from uuid import UUID

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

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            id=UUID(data["id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
