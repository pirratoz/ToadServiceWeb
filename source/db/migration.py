import os
import ujson
import datetime
import asyncio
import typing

import dotenv
from asyncpg import Connection

from source.db.connect import get_connection

MIGRATIONS_PATH = "source/db/migrations"
MIGRATIONS_JSON_PATH = "source/db/migrations/migrations.json"
MIGRATIONS_LIST: list[dict] = []
MIGRATIONS_IDS: set[str] = set()


async def load_accepted_migrations() -> None:
    global MIGRATIONS_LIST
    global MIGRATIONS_IDS
    if not os.path.exists(MIGRATIONS_JSON_PATH):
        with open(MIGRATIONS_JSON_PATH, "w") as fp:
            fp.write("[]")
        return None

    with open(MIGRATIONS_JSON_PATH, "r") as fp:
        MIGRATIONS_LIST = ujson.load(fp)
        MIGRATIONS_IDS = {migration["id"] for migration in MIGRATIONS_LIST}


async def get_not_accepted_migrations_file() -> typing.AsyncGenerator[tuple[str, str], None]:
    for file_name in sorted(os.listdir(MIGRATIONS_PATH)):
        if not file_name.endswith(".sql"):
            continue

        migration_id = file_name.split("_")[0]

        if migration_id in MIGRATIONS_IDS:
            print(f"[x] [skip] - {file_name}")
            continue

        yield file_name, migration_id


async def accept_migration(connection: Connection, file_name: str, migration_id: str) -> None:
    with open(f"{MIGRATIONS_PATH}/{file_name}", "r") as fp:
        sql_text = fp.read()
        await connection.execute(sql_text)
        print(f"[+] [accept] - {file_name}")
        MIGRATIONS_LIST.append({
            "id": migration_id,
            "name": file_name,
            "time": datetime.datetime.now().isoformat()
        })


async def save_migrations() -> None:
    with open(MIGRATIONS_JSON_PATH, "w") as fp:
        ujson.dump(MIGRATIONS_LIST, fp, indent=4)


async def main():
    dotenv.load_dotenv()

    connection = await get_connection()

    await load_accepted_migrations()
    async for file_name, migration_id in get_not_accepted_migrations_file():
        await accept_migration(connection, file_name, migration_id)

    await connection.close()

    await save_migrations()


if __name__ == "__main__":
    asyncio.run(main())
