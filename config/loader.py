from toml import load
from .entities import Config, ServerConfig


def load_config():
    conf = load("./config/application.toml")
    server_conf: ServerConfig = conf["server"]
    return Config(server=server_conf)
