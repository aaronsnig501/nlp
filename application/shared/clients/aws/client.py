from botocore.client import BaseClient
from botocore.exceptions import ClientError
from sanic.log import logger

from .entities import AWSResponse, SyntaxToken


class AWSComprehendClient:

    _client: BaseClient

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def detect_syntax(self, text: str, language_code: str) -> list[SyntaxToken]:
        """Detect Syntax

        Contacts AWS to get the syntactical breakdown of the provided text in the given
        language.

        Args:
            text (str): The text to determine the syntax of
            language_code (str): The code of the language

        Returns:
            list[SyntaxToken]: The syntax breakdown of the provided text
        """
        try:
            response = self._client.detect_syntax(
                Text=text, LanguageCode=language_code
            )
            response = AWSResponse(
                response["SyntaxTokens"], response["ResponseMetadata"]
            )
        except ClientError:
            logger.error("Couldn't detect syntax")
            raise
        else:
            return response.syntax_tokens