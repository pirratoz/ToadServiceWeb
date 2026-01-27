from os import getenv

from source.configs.base_config import BaseConfig


class WebConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.api_key: str = getenv("WEB_API_KEY", "NotSetUp")
