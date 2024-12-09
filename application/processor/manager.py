from sanic.log import logger

from application.shared.clients.decyphr.client import DecyphrNlpClient
from application.shared.clients.decyphr.types import NlpResponseDict
from .cache import ProcessorPubSub
from .entities import (
    ProcessRequestResponse,
    ProcessedTextResponse,
)
from .repository import ProcessorRepository

from .processors.aws.processor import AWSComprehendProcessor
from .processors.decyphr.processor import DecyphrNlpProcessor
from .processors.protocol import NlpProcessorProtocol


class ProcessorManager:
    """Processor manager

    Provides the interaction betweent the controller and the processors that process
    the data and the datastores, etc
    """

    _processors: dict[str, NlpProcessorProtocol]
    _pubsub: ProcessorPubSub
    _repository: ProcessorRepository
    _decyphr_client: DecyphrNlpClient

    def __init__(
        self,
        aws_processor: AWSComprehendProcessor,
        decyphr_processor: DecyphrNlpProcessor,
        pubsub: ProcessorPubSub,
        repository: ProcessorRepository,
        decyphr_client: DecyphrNlpClient,
    ) -> None:
        self._processors = {"aws": aws_processor, "decyphr": decyphr_processor}  # type: ignore
        self._pubsub = pubsub
        self._repository = repository
        self._decyphr_client = decyphr_client

    async def handle_processing(
        self, text: str, language_code: str, processor_name: str, client_id: str
    ) -> ProcessedTextResponse:
        """Handle processing

        Handle the processing of the processor request

        Args:
            text (str): The text to process
            language_code (str): The ISO 3166-1 alpha-2 code of the text language
            processor_name (str): The name of the processor to use
            client_id (str): UUID identifier

        Returns:
            ProcessedTextResponse: The processed data
        """
        logger.info("Request received from UI")
        await self._pubsub.publish_request_received_message(client_id)
        processor: NlpProcessorProtocol = self._processors[processor_name]

        process_request = await self._repository.save_process_request(
            processor_name, language_code, client_id, text
        )

        response: NlpResponseDict = await self._decyphr_client.get_processed_text(
            text, language_code
        )

        normalised_data = await processor.normalise_and_post_process_data(response)
        logger.info("ProcessorManager: Response normalised")

        await self._repository.save_process_request_with_tokens(
            normalised_data.tokens, process_request
        )

        processed_text_response = ProcessedTextResponse(
            id=process_request.id,
            process_request=ProcessRequestResponse(
                processor=process_request.processor,
                language_code=process_request.language_code,
                client_id=process_request.client_id,
                text=process_request.text,
            ),
            tokens=normalised_data.tokens,
            analysis=normalised_data.analysis,
        )

        await self._pubsub.publish_request_processed_message(
            processed_text_response=processed_text_response,
            client_id=process_request.client_id,
        )

        return processed_text_response
