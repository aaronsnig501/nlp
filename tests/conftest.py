from asyncio import get_event_loop
from typing import Any

from boto3 import client
from botocore.client import BaseClient
from pytest import fixture

from application.shared.clients.decyphr.client import DecyphrNlpClient
from application.shared.processors.aws.entities import SyntaxToken
from application.shared.processors.aws.processor import AWSComprehendProcessor
from application.shared.processors.decyphr.normaliser import DecyphrNlpNormaliser
from application.shared.processors.decyphr.processor import DecyphrNlpProcessor


@fixture(scope="session")
def event_loop():
    return get_event_loop()


@fixture
def aws_client() -> BaseClient:
    return client(
        "comprehend", "eu-west-1", aws_access_key_id="", aws_secret_access_key=""
    )


@fixture
def decyphr_client() -> DecyphrNlpClient:
    return DecyphrNlpClient("")


@fixture
def decyphr_normaliser() -> DecyphrNlpNormaliser:
    return DecyphrNlpNormaliser()


@fixture
def comprehend_client(aws_client: BaseClient) -> AWSComprehendProcessor:
    return AWSComprehendProcessor(aws_client)


@fixture
def decyphr_processor(
    decyphr_client: DecyphrNlpClient, decyphr_normaliser: DecyphrNlpNormaliser
) -> DecyphrNlpProcessor:
    return DecyphrNlpProcessor(decyphr_client, decyphr_normaliser)


@fixture
def aws_response_data() -> dict[str, Any]:
    return {
        "SyntaxTokens": [
            {
                "TokenId": "1",
                "Text": "hi",
                "BeginOffset": 0,
                "EndOffset": 10,
                "PartOfSpeech": {"Score": 0.123456, "Tag": "NOUN"},
            }
        ],
        "ResponseMetadata": {
            "RequestId": "123",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": 1,
                "content-type": "application/json",
                "content-length": "10",
                "date": "123",
            },
            "RetryAttempts": 1,
        },
    }


@fixture
def detect_syntax_return_value(aws_response_data: dict[str, Any]) -> list[SyntaxToken]:
    return [
        SyntaxToken(
            token_id=aws_response_data["SyntaxTokens"][0]["TokenId"],
            text=aws_response_data["SyntaxTokens"][0]["Text"],
            begin_offset=aws_response_data["SyntaxTokens"][0]["BeginOffset"],
            end_offset=aws_response_data["SyntaxTokens"][0]["EndOffset"],
            part_of_speech=aws_response_data["SyntaxTokens"][0]["PartOfSpeech"],
        )
    ]
