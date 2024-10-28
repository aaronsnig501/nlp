from unittest.mock import create_autospec

from pytest import mark

from application.pos_tagging.cache import PoSPubSub, Redis
from application.shared.clients.aws.entities import SyntaxToken
from application.shared.enums.message_types import MessageTypes


class TestCache:

    @mark.asyncio
    async def test_publish_received_message(self) -> None:
        mock_redis = create_autospec(Redis)
        pubsub = PoSPubSub(mock_redis)

        await pubsub.publish_request_received_message()

        mock_redis.publish_message.assert_awaited_with(
            {
                "message_type": MessageTypes.REQUEST_RECEIVED.value
            }
        )

    @mark.asyncio
    async def test_publish_request_processed_message(
        self, detect_syntax_return_value: list[SyntaxToken]
    ) -> None:
        mock_redis = create_autospec(Redis)
        pubsub = PoSPubSub(mock_redis)

        await pubsub.publish_request_processed_message(detect_syntax_return_value)

        mock_redis.publish_message.assert_awaited_with(
            {
                "message_type": MessageTypes.REQUEST_PROCESSED.value,
                "syntax_tokens": [
                    {
                        "token_id": "1",
                        "text": "hi",
                        "begin_offset": 0,
                        "end_offset": 10,
                        "part_of_speech": {
                            "tag": "NOUN",
                            "score": 0.123456
                        }
                    }
                ]
            }
        )
