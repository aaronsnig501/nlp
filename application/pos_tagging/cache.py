from dataclasses import asdict
from application.shared.clients.aws.entities import SyntaxToken
from application.shared.enums.message_types import MessageTypes
from application.shared.redis import Redis


class PoSPubSub:

    _redis: Redis

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def publish_request_received_message(self, client_id: str) -> None:
        """Publish the `REQUEST_RECEIVED` message"""
        await self._redis.publish_message(
            {
                "message_type": MessageTypes.REQUEST_RECEIVED.value
            },
            client_id
        )

    async def publish_request_processed_message(
        self, syntax_tokens: list[SyntaxToken], client_id: str
    ) -> None:
        """Publish request processed message

        Publish the `REQUEST_PROCESSED` message with the syntax tokens

        Args:
            syntax_tokens (list[SyntaxToken]): The data to publish
        """
        await self._redis.publish_message(
            {
                "message_type": MessageTypes.REQUEST_PROCESSED.value,
                "syntax_tokens": [asdict(syntax_token) for syntax_token in syntax_tokens]
            },
            client_id=client_id
        )
