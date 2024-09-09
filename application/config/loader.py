from toml import load
from .entities import Config, ServerConfig


def load_config():
    conf = load("./application/config/application.toml")
    server_conf: ServerConfig = ServerConfig(**conf["server"])
    return Config(server=server_conf)
