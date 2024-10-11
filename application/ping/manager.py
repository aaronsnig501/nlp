from asyncio import gather

from application.shared.redis import Redis
from .entities import HealthStatus


class PingManager:

    _redis: Redis

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def _perform_application_health_check(self) -> HealthStatus:
        """Perform application health check

        Ensure that the application is running

        Returns:
            HealthStatus: The health status of the application
        """
        return HealthStatus(name="application", is_healthy=True)

    async def _perform_redis_health_check(self) -> HealthStatus:
        """Perform redis health check

        Ensure that redis is running

        Returns:
            HealthStatus: The health status of redis
        """
        return HealthStatus(name="redis", is_healthy=await self._redis.health_check())

    async def get_health_status(self) -> list[HealthStatus]:
        """Get health status

        Get the health status of the application
        """
        health = await gather(
            self._perform_application_health_check(),
            self._perform_redis_health_check()
        )

        return list(health)

