from os import environ
from .entities import AWSConfig, Config, ServerConfig


def load_config():
    server_conf: ServerConfig = ServerConfig(
        host=environ.get("HOST", "0.0.0.0"),
        port=int(environ.get("PORT", 80))
    )
    aws_config: AWSConfig = AWSConfig(
        aws_access_key=environ["AWS_ACCESS_KEY"],
        aws_secret_key=environ["AWS_SECRET_KEY"]
    )
    return Config(server=server_conf, aws=aws_config)
