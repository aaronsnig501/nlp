from dataclasses import dataclass


@dataclass
class Token:
    text: str
    tag: str
    display_name: str


@dataclass
class Tokens:
    tokens: list[Token]


@dataclass
class Assessment:
    tokens: list[str]
    mood: str
    bias: str


@dataclass
class SentimentAnalysis:
    text: str
    mood: str
    bias: str
    assessment: list[Assessment]


@dataclass
class NormalisedNlp:
    tokens: list[Token]
    analysis: SentimentAnalysis
