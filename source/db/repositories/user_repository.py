from source.db.repositories.base_repository import BaseRepository
from source.db.repositories.settings_repository import SettingsRepository
from asyncpg import Connection

from datetime import (
    datetime,
    timezone
)

from source.dto import (
    UserInfo,
)


class UserRepository(BaseRepository):
    def __init__(self, connection: Connection):
        super().__init__(connection)

    async def create_user(self, user_id: int) -> UserInfo:
        trial_interval = await SettingsRepository(self.connection).get_trial_interval()
        paid_until = datetime.now(timezone.utc) + trial_interval
        record = await self.connection.fetchrow("INSERT INTO users (id, paid_until) VALUES ($1, $2) RETURNING *", user_id, paid_until)
        return UserInfo.load_from_record(record)

    async def update_vip_status(self, user_id: int, is_vip: bool) -> UserInfo:
        sql = """
        UPDATE users
        SET is_vip = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, is_vip, user_id)
        return UserInfo.load_from_record(record)

    async def update_ban_status(self, user_id: int, is_banned: bool) -> UserInfo:
        sql = """
        UPDATE users
        SET is_banned = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, is_banned, user_id)
        return UserInfo.load_from_record(record)
    
    async def update_calculate_status(self, user_id: int, is_calculate: bool) -> UserInfo:
        sql = """
        UPDATE users
        SET is_calculate = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, is_calculate, user_id)
        return UserInfo.load_from_record(record)
