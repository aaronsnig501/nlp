from os import environ

from .entities import (
    AWSConfig,
    Config,
    DatabaseConfig,
    NlpConfig,
    RedisConfig,
    ServerConfig,
)


def load_config():
    server_conf: ServerConfig = ServerConfig(
        host=environ.get("HOST", "0.0.0.0"), port=int(environ.get("PORT", 80))
    )
    aws_config: AWSConfig = AWSConfig(
        aws_access_key=environ["AWS_ACCESS_KEY"],
        aws_secret_key=environ["AWS_SECRET_KEY"],
    )
    redis_config: RedisConfig = RedisConfig(
        uri=environ["REDIS_URI"], channel=environ["NLP_REDIS_CHANNEL"]
    )
    db_config: DatabaseConfig = DatabaseConfig(uri=environ["MARIA_DB_URI"])
    nlp_config: NlpConfig = NlpConfig(url=environ["NLP_URL"])
    return Config(
        server=server_conf,
        aws=aws_config,
        redis=redis_config,
        database=db_config,
        nlp=nlp_config,
    )
