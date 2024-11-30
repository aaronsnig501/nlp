from dataclasses import asdict

from redis.asyncio import Redis as RedisPy
from sanic import Sanic
from sanic.log import LOGGING_CONFIG_DEFAULTS, logger
from sanic.request import Request as SanicRequest
from sanic.response import BaseHTTPResponse as SanicResponse
from tortoise.contrib.sanic import register_tortoise

from application.ping import register_ping_blueprint
from application.processor import register_processor_blueprint
from application.support import register_support_blueprint
from application.shared.redis import Redis
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

register_ping_blueprint(app, redis)
register_processor_blueprint(app, redis)
register_support_blueprint(app)


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
            "application.processor.models",
            "application.support.models",
        ]
    },
    generate_schemas=False,
)
