from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from dating.auth.dependencies import CurrentUser
from dating.candidates.schemas import ResponseCandidateSchema
from dating.candidates.services.feed import CandidateFeedService
from dating.schemas import ApiResponse

router = APIRouter(route_class=DishkaRoute, tags=["candidates"])
dev_router = APIRouter(route_class=DishkaRoute, tags=["candidates", "dev"])


@router.get("/next", response_model=ApiResponse[ResponseCandidateSchema | None])
async def get_next_candidate(
    user_id: CurrentUser, service: FromDishka[CandidateFeedService]
) -> ApiResponse[ResponseCandidateSchema | None]:
    candidate = await service.next_candidate(user_id)

    candidate_schema = ResponseCandidateSchema.from_dto(candidate) if candidate else None
    return ApiResponse(data=candidate_schema)


@dev_router.post("/generate", deprecated=True)
async def generate_candidates(
    user_id: CurrentUser, service: FromDishka[CandidateFeedService]
) -> None:
    await service.generate_candidates(user_id)


@dev_router.get("/count", deprecated=True)
async def get_candidates_count(
    user_id: CurrentUser, service: FromDishka[CandidateFeedService]
) -> int:
    return await service.get_candidate_pool_size(user_id)
