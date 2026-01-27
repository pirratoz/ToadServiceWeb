from os import getenv

from source.configs.base_config import BaseConfig


class JwtConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.public_key_path: str = getenv("JWT_PUBLIC_KEY_PATH", "NotSetUp")
        self.private_key_path: str = getenv("JWT_PRIVATE_KEY_PATH", "NotSetUp")
        self.access_token_exp_minutes: int = int(getenv("JWT_ACCESS_TOKEN_EXP_MINUTES", "5"))
        self.algorithm: str = getenv("JWT_ALGORITHM", "NotSetUp")
