from .cache import ProcessorPubSub
from .entities import (
    ProcessRequestResponse,
    ProcessRequestTokensResponse,
    TokenResponse,
)
from .repository import ProcessorRepository

from .processors.aws.processor import AWSComprehendProcessor
from .processors.decyphr.processor import DecyphrNlpProcessor
from .processors.entities import Tokens
from .processors.protocol import NlpProcessorProtocol


class ProcessorManager:
    """Processor manager

    Provides the interaction betweent the controller and the processors that process
    the data and the datastores, etc
    """

    _processors: dict[str, NlpProcessorProtocol]
    _pubsub: ProcessorPubSub
    _repository: ProcessorRepository

    def __init__(
        self,
        aws_processor: AWSComprehendProcessor,
        decyphr_processor: DecyphrNlpProcessor,
        pubsub: ProcessorPubSub,
        repository: ProcessorRepository,
    ) -> None:
        self._processors = {"aws": aws_processor, "decyphr": decyphr_processor}  # type: ignore
        self._pubsub = pubsub
        self._repository = repository

    async def process_pos_tagging(
        self,
        text: str,
        language_code: str,
        processor_name: str,
        client_id: str,
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
        processor: NlpProcessorProtocol = self._processors[processor_name]

        process_request = await self._repository.save_process_request(
            processor_name, language_code, client_id
        )

        syntax_tokens: Tokens = await processor.detect_syntax(text, language_code)

        tokens = await self._repository.save_process_request_with_tokens(
            syntax_tokens.tokens, process_request
        )

        process_request_with_tokens = ProcessRequestTokensResponse(
            id=process_request.id,
            process_request=ProcessRequestResponse(
                processor=processor_name,
                language_code=language_code,
                client_id=client_id,
            ),
            tokens=[TokenResponse(word=token.word, tag=token.tag) for token in tokens],
        )

        await self._pubsub.publish_request_processed_message(
            process_request_tokens=process_request_with_tokens, client_id=client_id
        )
        return process_request_with_tokens
