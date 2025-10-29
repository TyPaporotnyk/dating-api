from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from dating.auth.services.jwt import JWTService


class ServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_jwt_service(self, redis: Redis) -> JWTService:
        return JWTService(redis=redis)
