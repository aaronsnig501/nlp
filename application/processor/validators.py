from dataclasses import dataclass


@dataclass
class ProcessorRequestBody:
    text: str
    language: str
    processor: str
    client_id: str
