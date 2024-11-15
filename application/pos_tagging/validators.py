from dataclasses import dataclass


@dataclass
class PoSTaggingRequestBody:
    text: str
    language: str
    processor: str
    client_id: str
