from sanic import Sanic

from config.loader import load_config
from config.entities import Config

from application.ping.controllers import bp as ping_blueprint
from application.ping.manager import PingManager

app = Sanic("nlp")
app.blueprint(ping_blueprint)
config: Config = load_config()

app.ext.add_dependency(PingManager)

app.ext.openapi.describe(
    "Natural Language Processing API",
    version="0.1"
)


if __name__ == "__main__":
    app.run(host=config.server.host, port=config.server.port)
