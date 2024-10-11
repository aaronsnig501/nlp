from typing import Any
from unittest.mock import create_autospec

from pytest import mark
from application.pos_tagging.managers import PoSTaggingManager, AWSComprehendClient
from application.pos_tagging.cache import PoSPubSub
from application.shared.clients.aws.entities import SyntaxToken


class TestPoSTaggingManager:

    @mark.asyncio
    async def test_detect_syntax(
        self,
        mocker: Any,
        detect_syntax_return_value: list[SyntaxToken],
        comprehend_client: AWSComprehendClient
    ) -> None:
        aws_comprehend_mock = mocker.patch.object(
            AWSComprehendClient, "detect_syntax",
        )
        aws_comprehend_mock.return_value = detect_syntax_return_value

        pubsub_mock = create_autospec(PoSPubSub)
        manager = PoSTaggingManager(comprehend_client, pubsub_mock)
        assert (
            await manager.process_pos_tagging("hi", "en", "aws")
            == detect_syntax_return_value
        )
        aws_comprehend_mock.assert_called_with("hi", "en")
        pubsub_mock.publish_request_received_message.assert_awaited()
        pubsub_mock.publish_request_processed_message.assert_awaited()
