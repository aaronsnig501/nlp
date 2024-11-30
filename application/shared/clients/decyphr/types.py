from typing import TypedDict


class Tags(TypedDict):
    token: str
    tag: str


class NlpTaggingResponse(TypedDict):
    tags: list[Tags]
