from sanic import Sanic
from sanic.response import json

from config.loader import load_config
from config.entities import Config

app = Sanic("nlp")
config: Config = load_config()


@app.get("/")
async def hello(request):
    return json({"message": "OK"})


if __name__ == "__main__":
    app.run(host=config.server["host"], port=config.server["port"])
