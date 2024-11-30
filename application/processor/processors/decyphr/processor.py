from application.shared.clients.decyphr.client import DecyphrNlpClient

from .normaliser import DecyphrNlpNormaliser
from application.processor.processors.entities import Tokens


class DecyphrNlpProcessor:
    _client: DecyphrNlpClient
    _normaliser: DecyphrNlpNormaliser

    def __init__(
        self, client: DecyphrNlpClient, normaliser: DecyphrNlpNormaliser
    ) -> None:
        self._client = client
        self._normaliser = normaliser

    async def detect_syntax(self, text: str, language_code: str) -> Tokens:
        return self._normaliser.normalise(
            await self._client.process_text(text, language_code)
        )
