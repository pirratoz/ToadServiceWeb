from os import getenv

from source.configs.base_config import BaseConfig


class TgConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.token: str = getenv("TG_TOKEN", "NotSetUp")
