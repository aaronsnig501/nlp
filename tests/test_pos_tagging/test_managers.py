from typing import Any
from unittest.mock import create_autospec

from pytest import mark

from application.pos_tagging.cache import PoSPubSub
from application.pos_tagging.managers import PoSTaggingManager
from application.shared.processors.aws.entities import SyntaxToken
from application.shared.processors.aws.processor import AWSComprehendProcessor
from application.shared.processors.decyphr.processor import DecyphrNlpProcessor


class TestPoSTaggingManager:
    @mark.asyncio
    async def test_detect_syntax(
        self,
        mocker: Any,
        detect_syntax_return_value: list[SyntaxToken],
        aws_processor: AWSComprehendProcessor,
        decyphr_processor: DecyphrNlpProcessor,
    ) -> None:
        aws_comprehend_mock = mocker.patch.object(
            AWSComprehendProcessor,
            "detect_syntax",
        )
        aws_comprehend_mock.return_value = detect_syntax_return_value

        pubsub_mock = create_autospec(PoSPubSub)
        manager = PoSTaggingManager(aws_processor, decyphr_processor, pubsub_mock)
        assert (
            await manager.process_pos_tagging("hi", "en", "aws", "123")
            == detect_syntax_return_value
        )
        aws_comprehend_mock.assert_called_with("hi", "en")
        pubsub_mock.publish_request_received_message.assert_awaited()
        pubsub_mock.publish_request_processed_message.assert_awaited()
