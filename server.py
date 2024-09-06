from sanic import Sanic
from sanic.response import text

app = Sanic("nlp")


@app.get("/")
async def hello(request):
    return text("OK!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
