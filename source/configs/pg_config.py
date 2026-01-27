from os import getenv

from source.configs.base_config import BaseConfig


class PgConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.host: str = getenv("PG_HOST", "NotSetUp")
        self.port: int = int(getenv("PG_PORT", "5432"))
        self.user: str = getenv("PG_USER", "NotSetUp")
        self.password: str = getenv("PG_PASS", "NotSetUp")
        self.base: str = getenv("PG_BASE", "NotSetUp")
