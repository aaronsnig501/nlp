from application.shared.clients.aws.client import AWSComprehendClient
from application.shared.clients.aws.entities import SyntaxToken
from application.shared.clients.protocol import NlpClientProtocol


class PoSTaggingManager:
    """PoS Tagging Manager

    The manager responsible for performing the part of speech tagging for a given piece
    of text from a specified provider (i.e. AWS Comprehend, Google NLP, etc)
    """

    _clients: dict[str, NlpClientProtocol]

    def __init__(self, aws_client: AWSComprehendClient) -> None:
        self._clients = {
            "aws": aws_client
        }

    def process_pos_tagging(
        self, text: str, language_code: str, processor: str
    ) -> list[SyntaxToken]:
        """Process PoS Tagging

        Args:
            text (str): The text to be processed
            language_code (str): The code of the language used in the text
            processor (str): The name of the processor to use

        Returns:
            list[SyntaxToken]: The syntax breakdown of the provided text
        """
        client = self._clients[processor]
        return client.detect_syntax(text, language_code)
