from dataclasses import dataclass


@dataclass
class Token:
    text: str
    tag: str


@dataclass
class Tokens:
    tokens: list[Token]
