from sanic import Sanic

from application.shared.redis import Redis
from .controllers import bp as PingController
from .manager import PingManager


def register_ping_blueprint(app: Sanic, redis: Redis) -> None:
    app.blueprint(PingController)
    app.ext.dependency(PingManager(redis))
