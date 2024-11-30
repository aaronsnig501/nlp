from dataclasses import asdict

from boto3 import client
from redis.asyncio import Redis as RedisPy
from sanic import Sanic
from sanic.log import LOGGING_CONFIG_DEFAULTS, logger
from sanic.request import Request as SanicRequest
from sanic.response import BaseHTTPResponse as SanicResponse
from tortoise.contrib.sanic import register_tortoise

from application.ping.controllers import bp as ping_blueprint
from application.ping.manager import PingManager
from application.pos_tagging.cache import PoSPubSub
from application.pos_tagging.controllers import bp as pos_tagging_blueprint
from application.pos_tagging.managers import PoSTaggingManager
from application.pos_tagging.repository import PoSTaggingRepository
from application.shared.clients.decyphr.client import DecyphrNlpClient
from application.shared.processors.aws.processor import AWSComprehendProcessor
from application.shared.processors.decyphr.normaliser import DecyphrNlpNormaliser
from application.shared.processors.decyphr.processor import DecyphrNlpProcessor
from application.shared.redis import Redis
from application.support.controllers import bp as support_blueprint
from application.support.manager import SupportManager
from config.loader import load_config

LOGGING_CONFIG_DEFAULTS["formatters"] = {
    "generic": {"class": "sanic.logging.formatter.JSONFormatter"},
    "access": {"class": "sanic.logging.formatter.JSONFormatter"},
}

app = Sanic("nlp")
config = load_config()
app.config.update(asdict(config))

redis_connection = RedisPy.from_url(app.config["redis"]["uri"])

redis = Redis(redis_connection, app.config["redis"]["channel"])

TORTOISE_ORM = {
    "connections": {"default": app.config["database"]["uri"]},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "application.pos_tagging.models",
                "application.support.models",
            ],
            "default_connection": "default",
        }
    },
}

app.config.FALLBACK_ERROR_FORMAT = "json"

app.blueprint(ping_blueprint)
app.ext.dependency(PingManager(redis))

app.blueprint(pos_tagging_blueprint)
aws_processor = AWSComprehendProcessor(
    client=client(
        "comprehend",
        "eu-west-1",
        aws_access_key_id=config.aws.aws_access_key,
        aws_secret_access_key=config.aws.aws_secret_key,
    )
)
decyphr_processor = DecyphrNlpProcessor(
    DecyphrNlpClient("http://nlp:80/"), DecyphrNlpNormaliser()
)
pos_pubsub = PoSPubSub(redis)
tagging_manager = PoSTaggingManager(
    aws_processor=aws_processor,
    decyphr_processor=decyphr_processor,
    pubsub=pos_pubsub,
    repository=PoSTaggingRepository(),
)
app.ext.dependency(tagging_manager, "tagging_manager")

support_manager = SupportManager()
app.blueprint(support_blueprint)
app.ext.dependency(support_manager)

app.ext.openapi.describe("Natural Language Processing API", version="0.1")


@app.listener("before_server_start")
async def before_server_start(app, loop):
    app.ctx.redis = redis


@app.middleware("request")
async def callback_request(request: SanicRequest) -> None:
    logger.info(f"Request {request.path} received")


@app.middleware("response")
async def callback_response(request: SanicRequest, _: SanicResponse) -> None:
    logger.info(f"Request {request.path} processing finished")


register_tortoise(
    app,
    db_url=TORTOISE_ORM["connections"]["default"],
    modules={
        "models": [
            "application.pos_tagging.models",
            "application.support.models",
        ]
    },
    generate_schemas=False,
)
