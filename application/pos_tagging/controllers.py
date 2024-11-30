from dataclasses import asdict

from sanic import Blueprint
from sanic.request import Request as SanicRequest
from sanic.response import BaseHTTPResponse as SanicResponse
from sanic.response import json
from sanic_ext import openapi, validate

from application.pos_tagging.entities import ProcessRequestTokensResponse
from application.shared.processors.aws.entities import SyntaxToken

from .managers import PoSTaggingManager
from .validators import PoSTaggingRequestBody

bp = Blueprint("pos_tagging", url_prefix="/api/pos")


@bp.post("/tagging")
@validate(json=PoSTaggingRequestBody)
@openapi.summary("Perform PoS Tagging")
@openapi.body({"application/json": PoSTaggingRequestBody})
@openapi.response(
    200,
    {"application/json": list[SyntaxToken]},
    "The syntactical breakdown of the provided text",
)
async def pos_tagging(
    _: SanicRequest,
    body: PoSTaggingRequestBody,
    tagging_manager: PoSTaggingManager,
) -> SanicResponse:
    """PoS Tagging

    Determine the parts of speech of the provided text, from the given language code,
    using the provided provider (AWS Comprehend, Google NLP, etc)

    Example Usage:
        ```sh
        curl --header "Content-Type: application/json" \
            --request POST \
            --data '{"text": "hello", "language": "en", "processor": "aws"}' \
            http://localhost:8000/api/pos/tagging | jq
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
        await tagging_manager.process_pos_tagging(
            text=body.text,
            language_code=body.language,
            processor_name=body.processor,
            client_id=body.client_id,
        )
    )

    return json(asdict(process_requests))
