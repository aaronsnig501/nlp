from sanic import Blueprint
from sanic.response import json, BaseHTTPResponse as SanicResponse
from sanic.request import Request as SanicRequest

from .manager import SupportManager

bp = Blueprint("support", url_prefix="/api/support")


@bp.get("/part-of-speech-tagging/languages/<service>")
async def pos_tagging_service_language_support(
    _: SanicRequest, support_manager: SupportManager, service: str
) -> SanicResponse:
    return json(await support_manager.get_supported_languages(service))