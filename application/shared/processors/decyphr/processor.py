from application.shared.clients.decyphr.client import DecyphrNlpClient
from application.shared.processors.decyphr.normaliser import DecyphrNlpNormaliser
from application.shared.processors.entities import Tokens


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
            await self._client.get_part_of_speech_tags(text, language_code)
        )
