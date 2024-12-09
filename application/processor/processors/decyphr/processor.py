from application.shared.clients.decyphr.types import NlpResponseDict

from .normaliser import DecyphrNlpNormaliser
from application.processor.processors.entities import NormalisedNlp


class DecyphrNlpProcessor:
    _normaliser: DecyphrNlpNormaliser

    def __init__(self, normaliser: DecyphrNlpNormaliser) -> None:
        self._normaliser = normaliser

    async def normalise_and_post_process_data(
        self, data: NlpResponseDict
    ) -> NormalisedNlp:
        return self._normaliser.normalise(data)
