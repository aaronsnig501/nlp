from typing import Any
from unittest.mock import AsyncMock
from orjson import dumps
from pytest import mark
from redis.exceptions import ConnectionError
from application.shared.redis import Redis, RedisConnection


class TestRedis:

    @mark.asyncio
    async def test_publish_message(self, mocker: Any) -> None:
        mock_redis_connection = mocker.patch.object(
            RedisConnection, "publish", new=AsyncMock()
        )
        redis = Redis(mock_redis_connection, "nlp")

        await redis.publish_message({"message_type": "test"})
        mock_redis_connection.publish.assert_awaited_with(
            "nlp", dumps({"message_type": "test"})
        )

    @mark.asyncio
    async def test_health_check_healthy(self, mocker: Any) -> None:
        mock_redis_connection = mocker.patch.object(
            RedisConnection, "ping", new=AsyncMock()
        )
        redis = Redis(mock_redis_connection, "nlp")

        assert await redis.health_check()
        mock_redis_connection.ping.assert_awaited()

    @mark.asyncio
    async def test_healthy_check_unhealthy(self, mocker: Any) -> None:
        mock_redis_connection = mocker.patch.object(
            RedisConnection, "ping", new=AsyncMock()
        )
        mock_redis_connection.ping.side_effect = ConnectionError
        redis = Redis(mock_redis_connection, "nlp")

        assert not await redis.health_check()
        mock_redis_connection.ping.assert_awaited()
