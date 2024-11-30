from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass
class PartOfSpeech:
    tag: str
    score: Decimal


@dataclass(init=False)
class SyntaxToken:
    token_id: int
    text: str
    begin_offset: int
    end_offset: int
    part_of_speech: PartOfSpeech

    def __init__(
        self,
        token_id: int,
        text: str,
        begin_offset: int,
        end_offset: int,
        part_of_speech: dict[str, Any],
    ) -> None:
        self.token_id = token_id
        self.text = text
        self.begin_offset = begin_offset
        self.end_offset = end_offset
        self.part_of_speech = PartOfSpeech(
            part_of_speech["Tag"], part_of_speech["Score"]
        )


@dataclass
class HTTPHeaders:
    x_amzn_requestid: str
    content_type: str
    content_length: str
    date: datetime


@dataclass(init=False)
class ResponseMetadata:
    request_id: str
    http_status_code: int
    http_headers: HTTPHeaders
    retry_attempts: int

    def __init__(
        self,
        request_id: str,
        http_status_code: int,
        http_headers: dict[str, Any],
        retry_attempts: int,
    ) -> None:
        self.request_id = request_id
        self.http_status_code = http_status_code
        self.http_headers = HTTPHeaders(
            x_amzn_requestid=http_headers["x-amzn-requestid"],
            content_type=http_headers["content-type"],
            content_length=http_headers["content-length"],
            date=http_headers["date"],
        )
        self.retry_attempts = retry_attempts


@dataclass(init=False)
class AWSResponse:
    syntax_tokens: list[SyntaxToken]
    response_metadata: ResponseMetadata

    def __init__(
        self, syntax_tokens: list[dict[str, Any]], response_metadata: dict[str, Any]
    ) -> None:
        self.syntax_tokens = [
            SyntaxToken(
                token_id=token["TokenId"],
                text=token["Text"],
                begin_offset=token["BeginOffset"],
                end_offset=token["EndOffset"],
                part_of_speech=token["PartOfSpeech"],
            )
            for token in syntax_tokens
        ]
        self.response_metadata = ResponseMetadata(
            request_id=response_metadata["RequestId"],
            http_status_code=response_metadata["HTTPStatusCode"],
            http_headers=response_metadata["HTTPHeaders"],
            retry_attempts=response_metadata["RetryAttempts"],
        )
