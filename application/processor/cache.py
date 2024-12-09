from dataclasses import asdict
from sanic.log import logger
from application.processor.entities import ProcessedTextResponse
from application.shared.enums.message_types import MessageTypes
from application.shared.redis import Redis


class ProcessorPubSub:
    _redis: Redis

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def publish_request_received_message(self, client_id: str) -> None:
        """Publish the `REQUEST_RECEIVED` message"""
        logger.info("ProcessorPubSub: Publishing REQUEST_RECEIVED to pubsub")
        await self._redis.publish_message(
            {"message_type": MessageTypes.REQUEST_RECEIVED.value}, client_id
        )

    async def publish_request_processed_message(
        self, processed_text_response: ProcessedTextResponse, client_id: str
    ) -> None:
        """Publish request processed message

        Publish the `REQUEST_PROCESSED` message with the syntax tokens

        Args:
            processed_text_response (ProcessedTextResponse): The data to publish
        """
        logger.info("ProcessorPubSub: Publishing REQUEST_PROCESSED to pubsub")
        await self._redis.publish_message(
            {
                "message_type": MessageTypes.REQUEST_PROCESSED.value,
                "process_request_tokens": asdict(processed_text_response),
            },
            client_id=client_id,
        )
