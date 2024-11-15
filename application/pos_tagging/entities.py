from dataclasses import dataclass


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
