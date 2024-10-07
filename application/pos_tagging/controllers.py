from dataclasses import asdict
from typing import Any

from sanic import Blueprint
from sanic.response import json
from sanic_ext import openapi, validate
from sanic.request import Request as SanicRequest
from sanic.response import BaseHTTPResponse as SanicResponse

from .managers import PoSTaggingManager
from .validators import PoSTaggingRequestBody
from application.shared.clients.aws.client import SyntaxToken

bp = Blueprint("pos_tagging", url_prefix="/api/pos")


@bp.post("/tagging")
@validate(json=PoSTaggingRequestBody)
@openapi.summary("Perform PoS Tagging")
@openapi.body({"application/json": PoSTaggingRequestBody})
@openapi.parameter()
@openapi.response(
    200,
    {"application/json": list[SyntaxToken]},
    "The syntactical breakdown of the provided text"
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
        curl --header "Content-Type: application/json" \                                                                                                                                         ─╯
            --request POST \
            --data '{"text": "hello", "language": "en", "processor": "aws"}' \
            http://localhost:8000/api/pos/tagging | jq
        ```

    Example Response:
        ```json
        [
            {
                "token_id": 1,
                "text": "hello",
                "begin_offset": 0,
                "end_offset": 5,
                "part_of_speech": {
                    "tag": "NOUN",
                    "score": 0.9960765242576599
                }
            }
        ]
        ```
    """
    syntax_tokens: list[SyntaxToken] = tagging_manager.process_pos_tagging(
        text=body.text, language_code=body.language, processor=body.processor
    )

    syntax_tokens_as_dict: list[dict[str, Any]] = [
        asdict(token) for token in syntax_tokens
    ]

    return json(syntax_tokens_as_dict)
