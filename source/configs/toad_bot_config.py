from os import getenv

from source.configs.base_config import BaseConfig


class ToadBotConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.path_tg_bot_sessions: str = getenv("PATH_TG_BOT_SESSIONS", "NotSetUp")
