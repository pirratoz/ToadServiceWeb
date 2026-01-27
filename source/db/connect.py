import asyncpg

from source.configs import PgConfig

def get_dsn() -> str:
    config = PgConfig()
    return f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.base}"


async def get_connection() -> asyncpg.Connection:
    connection = await asyncpg.connect(dsn=get_dsn())
    return connection
