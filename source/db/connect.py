from os import getenv

import asyncpg


def get_dsn() -> str:
    user = getenv("PG_USER")
    password = getenv("PG_PASS")
    host = getenv("PG_HOST")
    port = getenv("PG_PORT")
    base = getenv("PG_BASE")
    return f"postgresql://{user}:{password}@{host}:{port}/{base}"


async def get_connection() -> asyncpg.Connection:
    connection = await asyncpg.connect(dsn=get_dsn())
    return connection
