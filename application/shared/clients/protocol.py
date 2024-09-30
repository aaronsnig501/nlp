from typing import Protocol

from application.shared.clients.aws.entities import SyntaxToken


class NlpClientProtocol(Protocol):

    def detect_syntax(self, text: str, language_code: str) -> list[SyntaxToken]: # type: ignore
        """Detect Syntax

        Contacts NLP API to get the syntactical breakdown of the provided text in the
        given language.

        Args:
            text (str): The text to determine the syntax of
            language_code (str): The code of the language

        Returns:
            list[SyntaxToken]: The syntax breakdown of the provided text
        """
