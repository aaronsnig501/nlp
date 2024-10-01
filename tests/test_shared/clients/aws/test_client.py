from typing import Any

from botocore.client import BaseClient

from application.shared.clients.aws.client import AWSComprehendClient
from application.shared.clients.aws.entities import SyntaxToken


class TestAWSComprehendClient:

    def test_detect_syntax(
        self,
        mocker: Any,
        aws_response_data: dict[str, Any],
        detect_syntax_return_value: list[SyntaxToken],
        aws_client: BaseClient
    ) -> None:
        comprehend_client = AWSComprehendClient(client=aws_client)
        mocker.patch.object(aws_client, "detect_syntax", return_value=aws_response_data)
        assert (
            comprehend_client.detect_syntax("hi", "en") == detect_syntax_return_value
        )
