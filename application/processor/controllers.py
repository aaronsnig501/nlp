from dataclasses import asdict

from sanic import Blueprint
from sanic.request import Request as SanicRequest
from sanic.response import BaseHTTPResponse as SanicResponse
from sanic.response import json
from sanic_ext import validate

from application.processor.entities import ProcessRequestTokensResponse

from .manager import ProcessorManager
from .validators import ProcessorRequestBody

bp = Blueprint("processor", url_prefix="/api/processor")


@bp.post("/process")
@validate(json=ProcessorRequestBody)
async def processor(
    _: SanicRequest,
    body: ProcessorRequestBody,
    processor_manager: ProcessorManager,
) -> SanicResponse:
    """Natural language processor

    Processor the text provided to determine the syntax tags, sentiment analysis, NER,
    etc

    Example Usage:
        ```sh
        curl --header "Content-Type: application/json" \
            --request POST \
            --data '{"text": "hello", "language": "en", "processor": "aws"}' \
            http://localhost:8000/api/processor/process | jq
        ```

    Example Response:
        ```json
        {
            "id": 60,
            "process_request": {
                "processor": "aws",
                "language_code": "en",
                "client_id": "d807e048-d118-4331-a8e6-d59cbe62cbd4"
            },
            "tokens": [
                {
                    "word": "hello",
                    "tag": "NOUN"
                },
            ]
        }
        ```
    """
    process_requests: ProcessRequestTokensResponse = (
        await processor_manager.process_pos_tagging(
            text=body.text,
            language_code=body.language,
            processor_name=body.processor,
            client_id=body.client_id,
        )
    )

    return json(asdict(process_requests))
