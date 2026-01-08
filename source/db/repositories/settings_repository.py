from datetime import timedelta

from source.db.repositories.base_repository import BaseRepository
from asyncpg import Connection

from source.db.utils import parse_interval


class SettingsRepository(BaseRepository):
    def __init__(self, connection: Connection):
        super().__init__(connection)

    async def get_trial_interval(self) -> timedelta:
        trial_interval_str = await self.connection.fetchval("SELECT value FROM settings WHERE key = $1", "trial_interval")
        return parse_interval(trial_interval_str)
