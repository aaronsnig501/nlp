from boto3 import client

from sanic import Sanic
from sanic.log import logger, LOGGING_CONFIG_DEFAULTS
from sanic.request import Request as SanicRequest
from sanic.response import BaseHTTPResponse as SanicResponse

from application.ping.controllers import bp as ping_blueprint
from application.ping.manager import PingManager

from application.pos_tagging.controllers import bp as pos_tagging_blueprint
from application.pos_tagging.managers import PoSTaggingManager

from application.shared.clients.aws.client import AWSComprehendClient
from config.loader import load_config

LOGGING_CONFIG_DEFAULTS["formatters"] = {
    "generic": {
        "class": "sanic.logging.formatter.JSONFormatter"
    },
    "access": {
        "class": "sanic.logging.formatter.JSONFormatter"
    }
}

app = Sanic("nlp")

app.config.FALLBACK_ERROR_FORMAT = "json"

config = load_config()

app.blueprint(ping_blueprint)
app.ext.add_dependency(PingManager)

app.blueprint(pos_tagging_blueprint)
aws_client = AWSComprehendClient(
    client=client(
        "comprehend",
        "eu-west-1",
        aws_access_key_id=config.aws.aws_access_key,
        aws_secret_access_key=config.aws.aws_secret_key
    )
)
tagging_manager = PoSTaggingManager(aws_client=aws_client)
app.ext.dependency(aws_client)
app.ext.dependency(tagging_manager, "tagging_manager")

app.ext.openapi.describe(
    "Natural Language Processing API",
    version="0.1"
)

@app.middleware("request")
async def callback_request(request: SanicRequest) -> None:
    logger.info(f"Request {request.path} received")


@app.middleware("response")
async def callback_response(request: SanicRequest, response: SanicResponse) -> None:
    logger.info(f"Request {request.path} processing finished")
