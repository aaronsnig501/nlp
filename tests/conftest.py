from typing import Any
from application.shared.clients.aws.client import AWSComprehendClient
from pytest import fixture

from boto3 import client
from botocore.client import BaseClient
from application.shared.clients.aws.entities import SyntaxToken


@fixture
def aws_client() -> BaseClient:
    return client(
        "comprehend", "eu-west-1", aws_access_key_id="", aws_secret_access_key=""
    )


@fixture
def comprehend_client(aws_client: BaseClient) -> AWSComprehendClient:
    return AWSComprehendClient(aws_client)


@fixture
def aws_response_data() -> dict[str, Any]:
    return {
        "SyntaxTokens": [
            {
                "TokenId": "1",
                "Text": "hi",
                "BeginOffset": 0,
                "EndOffset": 10,
                "PartOfSpeech": {
                    "Score": 0.123456,
                    "Tag": "NOUN"
                }
            }
        ],
        "ResponseMetadata": {
            "RequestId": "123",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": 1,
                "content-type": "application/json",
                "content-length": "10",
                "date": "123"
            },
            "RetryAttempts": 1
        }
    }


@fixture
def detect_syntax_return_value(aws_response_data: dict[str, Any]) -> list[SyntaxToken]:
    return [
        SyntaxToken(
            token_id=aws_response_data["SyntaxTokens"][0]["TokenId"],
            text=aws_response_data["SyntaxTokens"][0]["Text"],
            begin_offset=aws_response_data["SyntaxTokens"][0]["BeginOffset"],
            end_offset=aws_response_data["SyntaxTokens"][0]["EndOffset"],
            part_of_speech=aws_response_data["SyntaxTokens"][0]["PartOfSpeech"]
        )
    ]
