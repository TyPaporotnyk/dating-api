from dishka import Provider, Scope, provide

from dating.auth.services.jwt import JWTService
from dating.candidates.services.feed import CandidateFeedService


class ServiceProvider(Provider):
    scope = Scope.APP

    get_jwt_service = provide(JWTService)

    get_candidate_feed_service = provide(CandidateFeedService, scope=Scope.REQUEST)
