from application.pos_tagging.cache import PoSPubSub
from application.shared.clients.aws.client import AWSComprehendClient
from application.shared.clients.aws.entities import SyntaxToken
from application.shared.clients.protocol import NlpClientProtocol


class PoSTaggingManager:
    """PoS Tagging Manager

    The manager responsible for performing the part of speech tagging for a given piece
    of text from a specified provider (i.e. AWS Comprehend, Google NLP, etc)
    """

    _clients: dict[str, NlpClientProtocol]
    _pubsub: PoSPubSub

    def __init__(self, aws_client: AWSComprehendClient, pubsub: PoSPubSub) -> None:
        self._clients = {
            "aws": aws_client
        }
        self._pubsub = pubsub

    async def process_pos_tagging(
        self,
        text: str,
        language_code: str,
        processor: str,
    ) -> list[SyntaxToken]:
        """Process PoS Tagging

        Process the text and also publish update messages to pubsub channel

        Args:
            text (str): The text to be processed
            language_code (str): The code of the language used in the text
            processor (str): The name of the processor to use

        Returns:
            list[SyntaxToken]: The syntax breakdown of the provided text
        """
        await self._pubsub.publish_request_received_message()
        client = self._clients[processor]
        syntax_tokens: list[SyntaxToken] = client.detect_syntax(text, language_code)
        await self._pubsub.publish_request_processed_message(
            syntax_tokens=syntax_tokens
        )
        return syntax_tokens