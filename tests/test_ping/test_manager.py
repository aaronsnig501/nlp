from typing import Any
from unittest.mock import create_autospec
from pytest import mark
from redis.asyncio import Redis as RedisConnection
from redis.exceptions import ConnectionError
from application.ping.entities import HealthStatus
from application.ping.manager import PingManager
from application.shared.redis import Redis


class TestPingManager:
    @mark.asyncio
    async def test_get_health_status(self, mocker: Any) -> None:
        redis_mock = create_autospec(Redis)
        mocker.patch.object(
            PingManager,
            "_perform_application_health_check",
            return_value=HealthStatus("application", True),
        )
        redis_mock.health_check.return_value = True

        manager = PingManager(redis_mock)
        assert await manager.get_health_status() == [
            HealthStatus("application", True),
            HealthStatus("redis", True)
        ]

    @mark.asyncio
    async def test_redis_health_check_healthy(self, mocker: Any) -> None:
        redis_mock = create_autospec(Redis)
        redis_mock.health_check.return_value = True

        manager = PingManager(redis_mock)

        assert (
            await manager._perform_redis_health_check() == HealthStatus("redis", True)
        )

    @mark.asyncio
    async def test_redis_health_check_unhealthy(self, mocker: Any) -> None:
        redis_connection_mock = create_autospec(RedisConnection)
        redis = Redis(redis_connection_mock, channel="nlp")
        redis_connection_mock.ping.side_effect = ConnectionError

        manager = PingManager(redis)

        assert (
            await manager._perform_redis_health_check() == HealthStatus("redis", False)
        )
