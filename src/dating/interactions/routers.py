from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from dating.auth.dependencies import CurrentUser
from dating.enums import InteractionType
from dating.interactions.interactors.match import CreateInteractionInteractor
from dating.schemas import ApiResponse

router = APIRouter(route_class=DishkaRoute, prefix="/users", tags=["interactions"])


@router.post("/{to_user_id}/like", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def like_user(
    to_user_id: UUID,
    current_user_id: CurrentUser,
    interactor: FromDishka[CreateInteractionInteractor],
) -> ApiResponse:
    interaction = await interactor(
        from_user_id=current_user_id,
        to_user_id=to_user_id,
        interaction_type=InteractionType.LIKE,
    )
    return ApiResponse(data=interaction)


@router.post(
    "/{to_user_id}/dislike", response_model=ApiResponse, status_code=status.HTTP_201_CREATED
)
async def dislike_user(
    to_user_id: UUID,
    current_user_id: CurrentUser,
    interactor: FromDishka[CreateInteractionInteractor],
) -> ApiResponse:
    interaction = await interactor(
        from_user_id=current_user_id,
        to_user_id=to_user_id,
        interaction_type=InteractionType.DISLIKE,
    )
    return ApiResponse(data=interaction)
