from typing import Any
from application.pos_tagging.managers import PoSTaggingManager, AWSComprehendClient
from application.shared.clients.aws.entities import SyntaxToken


class TestPoSTaggingManager:

    def test_detect_syntax(
        self,
        mocker: Any,
        detect_syntax_return_value: list[SyntaxToken],
        comprehend_client: AWSComprehendClient
    ) -> None:
        aws_comprehend_mock = mocker.patch.object(
            AWSComprehendClient, "detect_syntax",
        )
        aws_comprehend_mock.return_value = detect_syntax_return_value
        manager = PoSTaggingManager(comprehend_client)
        assert (
            manager.process_pos_tagging("hi", "en", "aws") == detect_syntax_return_value
        )
        aws_comprehend_mock.assert_called_with("hi", "en")
