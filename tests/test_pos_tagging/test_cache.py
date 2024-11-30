from unittest.mock import create_autospec

from pytest import mark

from application.processor.cache import ProcessorPubSub, Redis
from application.shared.enums.message_types import MessageTypes
from application.shared.processors.aws.entities import SyntaxToken


class TestCache:
    @mark.asyncio
    async def test_publish_received_message(self) -> None:
        mock_redis = create_autospec(Redis)
        pubsub = ProcessorPubSub(mock_redis)

        await pubsub.publish_request_received_message("123")

        mock_redis.publish_message.assert_awaited_with(
            {"message_type": MessageTypes.REQUEST_RECEIVED.value}, "123"
        )

    @mark.asyncio
    async def test_publish_request_processed_message(
        self, detect_syntax_return_value: list[SyntaxToken]
    ) -> None:
        mock_redis = create_autospec(Redis)
        pubsub = ProcessorPubSub(mock_redis)

        await pubsub.publish_request_processed_message(
            detect_syntax_return_value, "123"
        )

        mock_redis.publish_message.assert_awaited_with(
            {
                "message_type": MessageTypes.REQUEST_PROCESSED.value,
                "syntax_tokens": [
                    {
                        "token_id": "1",
                        "text": "hi",
                        "begin_offset": 0,
                        "end_offset": 10,
                        "part_of_speech": {"tag": "NOUN", "score": 0.123456},
                    }
                ],
            },
            "123",
        )
