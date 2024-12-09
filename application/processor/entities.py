from dataclasses import dataclass

from application.processor.processors.entities import Token
from application.processor.processors.entities import SentimentAnalysis


@dataclass
class TokenResponse:
    word: str
    tag: str


@dataclass
class ProcessRequestResponse:
    processor: str
    language_code: str
    client_id: str


@dataclass
class ProcessRequestTokensResponse:
    id: int
    process_request: ProcessRequestResponse
    tokens: list[TokenResponse]


@dataclass
class ProcessedTextResponse:
    id: int
    process_request: ProcessRequestResponse
    tokens: list[Token]
    analysis: SentimentAnalysis
