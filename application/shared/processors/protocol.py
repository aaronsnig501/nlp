from typing import Protocol

from .entities import Tokens


class NlpProcessorProtocol(Protocol):
    async def detect_syntax(self, text: str, language_code: str) -> Tokens:  # type: ignore
        """Detect Syntax

        Contacts NLP API to get the syntactical breakdown of the provided text in the
        given language.

        Args:
            text (str): The text to determine the syntax of
            language_code (str): The code of the language

        Returns:
            list[SyntaxToken]: The syntax breakdown of the provided text
        """
