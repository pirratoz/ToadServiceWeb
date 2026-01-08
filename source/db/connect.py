from os import getenv

import asyncpg


async def get_connection() -> asyncpg.Connection:
    user = getenv("PG_USER")
    password = getenv("PG_PASS")
    host = getenv("PG_HOST")
    port = getenv("PG_PORT")
    base = getenv("PG_BASE")
    connection = await asyncpg.connect(dsn=f"postgresql://{user}:{password}@{host}:{port}/{base}")
    return connection
