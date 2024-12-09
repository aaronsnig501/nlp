from aiohttp import ClientSession
from sanic.log import logger
from application.shared.clients.decyphr.types import NlpResponseDict


class DecyphrNlpClient:
    _base_url: str

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    async def get_processed_text(self, text: str, language: str) -> NlpResponseDict:
        """Get Processed Text

        Contact the Decyphr NLP service to process the text

        Args:
            text (str): The text to be processed
            language (str): The ISO 3166-1 alpha-2 of the text language

        Returns:
            NlpResponseDict: The data returned from the NLP service
        """
        async with ClientSession() as session:
            async with session.post(
                f"{self._base_url}api/processing",
                json={"text": text, "language": language},
            ) as resp:
                json_data = await resp.json()
                logger.info("DecyphrClient: Received NLP response")
                return json_data
