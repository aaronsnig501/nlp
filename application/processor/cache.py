from dataclasses import asdict
from application.processor.entities import ProcessRequestTokensResponse
from application.shared.enums.message_types import MessageTypes
from application.shared.redis import Redis


class ProcessorPubSub:
    _redis: Redis

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def publish_request_received_message(self, client_id: str) -> None:
        """Publish the `REQUEST_RECEIVED` message"""
        await self._redis.publish_message(
            {"message_type": MessageTypes.REQUEST_RECEIVED.value}, client_id
        )

    async def publish_request_processed_message(
        self, process_request_tokens: ProcessRequestTokensResponse, client_id: str
    ) -> None:
        """Publish request processed message

        Publish the `REQUEST_PROCESSED` message with the syntax tokens

        Args:
            process_request_tokens (ProcessRequestTokensResponse): The data to publish
        """
        await self._redis.publish_message(
            {
                "message_type": MessageTypes.REQUEST_PROCESSED.value,
                "process_request_tokens": asdict(process_request_tokens),
            },
            client_id=client_id,
        )
