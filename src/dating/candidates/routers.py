from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from dating.auth.dependencies import CurrentUser
from dating.candidates.interactors.search import SearchCandidatesInteractor
from dating.profiles.schemas import ResponseProfileSchema
from dating.schemas import ApiResponse

router = APIRouter(route_class=DishkaRoute, tags=["candidates"])


@router.get("", response_model=ApiResponse[list[ResponseProfileSchema]])
async def get_candidates(
    user_id: CurrentUser, interactor: FromDishka[SearchCandidatesInteractor]
) -> ApiResponse[list[ResponseProfileSchema]]:
    profiles = await interactor(user_id)

    return ApiResponse(data=[ResponseProfileSchema.from_dto(profile) for profile in profiles])
