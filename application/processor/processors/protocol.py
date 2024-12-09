from typing import Protocol

from application.shared.clients.decyphr.types import NlpResponseDict
from .entities import NormalisedNlp, Tokens


class NlpProcessorProtocol(Protocol):
    async def detect_syntax(self, data: NlpResponseDict) -> Tokens:  # type: ignore
        """Detect Syntax

        Contacts NLP API to get the syntactical breakdown of the provided text in the
        given language.

        Args:
            text (str): The text to determine the syntax of
            language_code (str): The code of the language

        Returns:
            list[SyntaxToken]: The syntax breakdown of the provided text
        """

    async def normalise_and_post_process_data(
        self, data: NlpResponseDict
    ) -> NormalisedNlp: ...
