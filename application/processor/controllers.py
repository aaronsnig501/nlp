from dataclasses import asdict

from sanic import Blueprint
from sanic.request import Request as SanicRequest
from sanic.response import BaseHTTPResponse as SanicResponse
from sanic.response import json
from sanic_ext import validate


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
        curl --request POST \
            --url http://localhost:8000/api/processor/process \
            --header 'Content-Type: application/json' \
            --data '{ \
                "language": "en",\
                "processor":"decyphr",\
                "text":"I really hate doing assignments on weekends so much!", \
                "client_id":"14807eb6-ad8c-4e75-a1e5-5d436d30da68" \
            }'
        ```

    Example Response:
        ```json
        {
            "id": 155,
            "process_request": {
                "processor": "decyphr",
                "language_code": "en",
                "client_id": "14807eb6-ad8c-4e75-a1e5-5d436d30da68"
            },
            "tokens": [
                {
                    "text": "I",
                    "tag": "PRON",
                    "display_name": "pronoun"
                },
                {
                    "text": "really",
                    "tag": "ADV",
                    "display_name": "adverb"
                },
                {
                    "text": "hate",
                    "tag": "VERB",
                    "display_name": "verb"
                },
                {
                    "text": "doing",
                    "tag": "VERB",
                    "display_name": "verb"
                },
                {
                    "text": "assignments",
                    "tag": "NOUN",
                    "display_name": "noun"
                },
                {
                    "text": "on",
                    "tag": "ADP",
                    "display_name": "adposition"
                },
                {
                    "text": "weekends",
                    "tag": "NOUN",
                    "display_name": "noun"
                },
                {
                    "text": "so",
                    "tag": "ADV",
                    "display_name": "adverb"
                },
                {
                    "text": "much",
                    "tag": "ADV",
                    "display_name": "adverb"
                },
                {
                    "text": "!",
                    "tag": "PUNCT",
                    "display_name": "punctuation"
                }
            ],
            "analysis": {
                "text": "I really hate doing assignments on weekends so much! ",
                "mood": "negative",
                "bias": "subjective",
                "assessment": [
                    {
                        "tokens": [
                            "really",
                            "hate"
                        ],
                        "mood": "negative",
                        "bias": "subjective"
                    },
                    {
                        "tokens": [
                            "much",
                            "!"
                        ],
                        "mood": "positive",
                        "bias": "objective"
                    }
                ]
            }
        }
        ```
    """
    process_requests = await processor_manager.handle_processing(
        text=body.text,
        language_code=body.language,
        processor_name=body.processor,
        client_id=body.client_id,
    )

    return json(asdict(process_requests))
