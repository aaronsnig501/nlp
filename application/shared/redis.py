from typing import Any
from orjson import dumps
from redis.asyncio import Redis as RedisConnection
from redis.exceptions import ConnectionError


class Redis:
    """Wrapper around the redis.asyncio Redis object with helpers"""

    _connection: RedisConnection
    _channel: str

    def __init__(self, connection: RedisConnection, channel: str) -> None:
        self._connection = connection
        self._channel = channel

    async def publish_message(self, message: dict[str, Any]) -> None:
        """Publish message

        Args:
            message (dict[str, Any]): The data structure to publish
        """
        await self._connection.publish(self._channel, dumps(message))

    async def health_check(self) -> bool:
        """Perform redis health check

        If ping is successful, return true, otherwise return fails

        Returns:
            bool: Flag that indicates if a connecation to redis can be made successfully
        """
        try:
            return bool(await self._connection.ping())
        except ConnectionError:
            return False
