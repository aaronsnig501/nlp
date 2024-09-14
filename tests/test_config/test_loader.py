from typing import Any
from config.loader import load_config
from config.entities import Config, ServerConfig


def test_load_config(mocker: Any):
    mocker.patch(
        "config.loader.load", return_value={"server": {"host": "0.0.0.0", "port": 8000}}
    )
    assert load_config() == Config(
        server=ServerConfig(host="0.0.0.0", port=8000)
    )
