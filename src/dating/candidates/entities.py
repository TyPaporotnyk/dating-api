from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from dating.entities import Entity


@dataclass(kw_only=True)
class Candidate(Entity):
    profile_id: UUID
    distance_between: int

    @classmethod
    def from_dict(cls, data: dict) -> "Candidate":
        return Candidate(
            id=UUID(data["id"]),
            profile_id=UUID(data["profile_id"]),
            distance_between=data["distance_between"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "profile_id": str(self.profile_id),
            "distance_between": self.distance_between,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
