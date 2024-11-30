from aiohttp import ClientSession

from application.shared.clients.decyphr.types import NlpTaggingResponse


class DecyphrNlpClient:
    _base_url: str

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    async def process_text(self, text: str, language: str) -> NlpTaggingResponse:
        async with ClientSession() as session:
            async with session.post(
                f"{self._base_url}api/processing",
                json={"text": text, "language": language},
            ) as resp:
                return await resp.json()
