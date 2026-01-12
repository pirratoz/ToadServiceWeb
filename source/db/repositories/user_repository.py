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

    async def get_user_by_id(self, user_id: int) -> UserInfo | None:
        record = await self.connection.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        if record:
            return UserInfo.load_from_record(record)
        return record

    async def create_user(self, user_id: int) -> UserInfo:
        trial_interval = await SettingsRepository(self.connection).get_trial_interval()
        paid_until = datetime.now(timezone.utc) + trial_interval
        record = await self.connection.fetchrow("INSERT INTO users (id, paid_until) VALUES ($1, $2) RETURNING *", user_id, paid_until)
        return UserInfo.load_from_record(record)

    async def update_api_id(self, user_id: int, api_id: int) -> UserInfo:
        sql = """
        UPDATE users
        SET api_id = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, api_id, user_id)
        return UserInfo.load_from_record(record)
    
    async def update_api_hash(self, user_id: int, api_hash: str) -> UserInfo:
        sql = """
        UPDATE users
        SET api_hash = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, api_hash, user_id)
        return UserInfo.load_from_record(record)
    
    async def update_phone(self, user_id: int, phone: str) -> UserInfo:
        sql = """
        UPDATE users
        SET phone = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, phone, user_id)
        return UserInfo.load_from_record(record)
    
    async def update_password_2fa(self, user_id: int, password_2fa: str) -> UserInfo:
        sql = """
        UPDATE users
        SET password_2fa = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, password_2fa, user_id)
        return UserInfo.load_from_record(record)

    async def update_chat_id(self, user_id: int, chat_id: int) -> UserInfo:
        sql = """
        UPDATE users
        SET chat_id = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, chat_id, user_id)
        return UserInfo.load_from_record(record)

    async def update_chat_title(self, user_id: int, chat_title: bool) -> UserInfo:
        sql = """
        UPDATE users
        SET chat_title = $1
        WHERE id = $2
        RETURNING *
        """
        record = await self.connection.fetchrow(sql, chat_title, user_id)
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
