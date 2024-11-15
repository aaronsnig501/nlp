from .cache import PoSPubSub
from .models import ProcessRequest, ProcessRequestTokens, Token
from .entities import TokenResponse, ProcessRequestResponse, ProcessRequestTokensResponse
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

    def __init__(
        self,
        aws_client: AWSComprehendClient,
        pubsub: PoSPubSub) -> None:
        self._clients = {
            "aws": aws_client
        }
        self._pubsub = pubsub

    async def process_pos_tagging(
        self, text: str, language_code: str, processor: str, client_id: str,
    ) -> ProcessRequestTokensResponse:
        """Process PoS Tagging

        Process the text and also publish update messages to pubsub channel

        Args:
            text (str): The text to be processed
            language_code (str): The code of the language used in the text
            processor (str): The name of the processor to use

        Returns:
            ProcessRequestTokensResponse: The syntax breakdown of the provided text
        """
        await self._pubsub.publish_request_received_message(client_id)
        client = self._clients[processor]

        process_request = ProcessRequest(
            processor=processor, language_code=language_code, client_id=client_id
        )
        await process_request.save()

        aws_tokens: list[SyntaxToken] = client.detect_syntax(text, language_code)

        tokens: list[Token] = []
        process_request_tokens: list[ProcessRequestTokens] = []
        for token in aws_tokens:
            token = Token(word=token.text, tag=token.part_of_speech.tag)
            await token.save()
            tokens.append(token)

        for token in tokens:
            process_request_tokens.append(
                ProcessRequestTokens(process_request=process_request, token=token)
            )
        await ProcessRequestTokens.bulk_create(process_request_tokens)

        process_request_with_tokens = ProcessRequestTokensResponse(
            id=process_request.id,
            process_request=ProcessRequestResponse(
                processor=processor,
                language_code=language_code,
                client_id=client_id
            ),
            tokens=[
                TokenResponse(word=token.word, tag=token.tag) for token in tokens
            ]
        )

        await self._pubsub.publish_request_processed_message(
            process_request_tokens=process_request_with_tokens, client_id=client_id
        )
        return process_request_with_tokens
