from typing import TypedDict


class TagsResponseDict(TypedDict):
    token: str
    tag: str


class AssessmentResponseDict(TypedDict):
    tokens: list[str]
    polarity: float
    subjectivity: float


class SentimentAnalysisResponseDict(TypedDict):
    text: str
    polarity: float
    subjectivity: float
    assessment: list[AssessmentResponseDict]


class NlpResponseDict(TypedDict):
    tags: list[TagsResponseDict]
    analysis: SentimentAnalysisResponseDict
