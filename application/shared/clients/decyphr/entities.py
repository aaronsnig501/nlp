from dataclasses import dataclass


@dataclass
class Tag:
    token: str
    tag: str

    def as_dict(self) -> dict[str, str]:
        return self.__dict__


@dataclass
class NlpResponseBody:
    tags: list[Tag]
