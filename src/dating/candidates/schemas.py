from uuid import UUID

from pydantic import BaseModel

from dating.candidates.entities import Candidate


class ResponseCandidateSchema(BaseModel):
    profile_id: UUID
    distance_between: int

    @classmethod
    def from_dto(cls, entity: Candidate) -> "ResponseCandidateSchema":
        return cls(profile_id=entity.profile_id, distance_between=entity.distance_between)
