from sanic import Sanic
from .controllers import bp as SupportController
from .manager import SupportManager


def register_support_blueprint(app: Sanic) -> None:
    app.blueprint(SupportController)
    app.ext.dependency(SupportManager())
