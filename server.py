from sanic import Sanic
from sanic.response import json

from application.config.loader import load_config
from application.config.entities import Config

from application.ping.controllers import bp as ping_blueprint
from application.ping.manager import PingManager

app = Sanic("nlp")
app.blueprint(ping_blueprint)
config: Config = load_config()

app.ext.add_dependency(PingManager)


@app.get("/")
async def hello(request):
    return json({"message": "Welcome to nlp"})


if __name__ == "__main__":
    app.run(host=config.server.host, port=config.server.port)
