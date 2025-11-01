import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request

from dating.auth.commands import CreateUserCommand, LoginUserCommand
from dating.auth.dependencies import CurrentUser
from dating.auth.exceptions import AuthError, UserAlreadyExist, UserNotFound
from dating.auth.interactors.login import LoginUserInteractor
from dating.auth.interactors.register import CreateUserInteractor
from dating.auth.interactors.verification_request import VerificationRequestInteractor
from dating.auth.interactors.verification_submit import VerificationSubmitInteractor
from dating.auth.schemas import (
    CreateUserSchema,
    LoginUserSchema,
    RefreshTokenSchema,
    ResponseUserSchema,
    TokenPairResponse,
    VerificationUserSubmitSchema,
)
from dating.auth.services.jwt import JWTService
from dating.limiter import limiter
from dating.schemas import ApiResponse, MessageSchema

logger = logging.getLogger(__name__)
auth_router = APIRouter(route_class=DishkaRoute, tags=["auth"])
user_router = APIRouter(route_class=DishkaRoute, tags=["users"])


@auth_router.post("/register", response_model=ApiResponse[TokenPairResponse])
async def create_user(
    data: CreateUserSchema, interaction: FromDishka[CreateUserInteractor]
) -> ApiResponse[TokenPairResponse]:
    command = CreateUserCommand(**data.model_dump())
    try:
        token_pair = await interaction(command=command)
    except UserAlreadyExist as e:
        logger.warning("User already exist", extra={"email": command.email})
        raise e

    logger.info("User registered successfully", extra={"email": command.email})
    return ApiResponse(data=TokenPairResponse.from_dto(token_pair))


@auth_router.post("/login", response_model=ApiResponse[TokenPairResponse])
async def login_user(
    data: LoginUserSchema, interactor: FromDishka[LoginUserInteractor]
) -> ApiResponse[TokenPairResponse]:
    command = LoginUserCommand(**data.model_dump())

    try:
        token_pair = await interactor(command=command)
    except (UserNotFound, AuthError) as e:
        logger.warning("User login failed: invalid credentials", extra={"email": command.email})
        raise e

    logger.info("User login successfully", extra={"email": command.email})
    return ApiResponse(data=TokenPairResponse.from_dto(token_pair))


@auth_router.post("/refresh", response_model=ApiResponse[TokenPairResponse])
async def refresh_token(
    data: RefreshTokenSchema, token_service: FromDishka[JWTService]
) -> ApiResponse[TokenPairResponse]:
    token_pair = await token_service.refresh_tokens(data.refresh_token)
    return ApiResponse(data=TokenPairResponse.from_dto(token_pair))


@user_router.get("/me", response_model=ApiResponse[ResponseUserSchema])
async def get_current_user(user: CurrentUser) -> ApiResponse[ResponseUserSchema]:
    return ApiResponse(data=ResponseUserSchema.from_dto(user))


@user_router.post("/verification/request", response_model=ApiResponse[MessageSchema])
@limiter.limit("1/minute")
async def verification_user_request(
    request: Request, user: CurrentUser, interactor: FromDishka[VerificationRequestInteractor]
) -> ApiResponse[MessageSchema]:
    await interactor(user_id=user.id)
    return ApiResponse(data=MessageSchema(message="Verification code has been send"))


@user_router.post("/verification/submit", response_model=ApiResponse[MessageSchema])
@limiter.limit("5/minute")
async def verification_user_submit(
    request: Request,
    user: CurrentUser,
    data: VerificationUserSubmitSchema,
    interactor: FromDishka[VerificationSubmitInteractor],
) -> ApiResponse[MessageSchema]:
    is_valid = await interactor(user_id=user.id, code=data.code)

    message = "User has been verified" if is_valid else "Provided code is not valid"

    return ApiResponse(data=MessageSchema(message=message))
