from source.db.repositories.base_repository import BaseRepository
from asyncpg import Connection


class HistoryPromocodesRepository(BaseRepository):
    def __init__(self, connection: Connection):
        super().__init__(connection)

    async def get_any(self) -> None:
        ...
