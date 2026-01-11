from datetime import datetime
from dataclasses import dataclass

from asyncpg import Record


@dataclass
class UserInfo:
    id: int
    is_banned: bool
    is_vip: bool
    is_calculate: bool
    paid_until: datetime
    chat_id: int
    chat_title: str

    @staticmethod
    def load_from_record(record: Record) -> "UserInfo":
        return UserInfo(
            id=record["id"],
            is_banned=record["is_banned"],
            is_vip=record["is_vip"],
            is_calculate=record["is_calculate"],
            paid_until=record["paid_until"],
            chat_id=record["chat_id"],
            chat_title=record["chat_title"]
        )

    def dump(self) -> dict:
        return {
            "id": self.id,
            "is_banned": self.is_banned,
            "is_vip": self.is_vip,
            "is_calculate": self.is_calculate,
            "paid_until": self.paid_until.isoformat(),
            "chat_id": self.chat_id,
            "chat_title": self.chat_title,
        }
