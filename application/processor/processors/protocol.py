from typing import Protocol

from application.shared.clients.decyphr.types import NlpResponseDict
from .entities import NormalisedNlp


class NlpProcessorProtocol(Protocol):
    async def normalise_and_post_process_data(
        self, data: NlpResponseDict
    ) -> NormalisedNlp:  # type: ignore
        """Normalise and post process data

        Perform the post processing on the data that is returned from the NLP provider
        to ensure that the data is normalised

        Args:
            data (NlpResponseDict): The data from the NLP provider

        Returns:
            NormalisedNlp: The normalised data
        """
