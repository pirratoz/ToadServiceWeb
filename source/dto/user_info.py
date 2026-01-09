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

    @staticmethod
    def load_from_record(record: Record) -> "UserInfo":
        return UserInfo(
            id=record["id"],
            is_banned=record["is_banned"],
            is_vip=record["is_vip"],
            is_calculate=record["is_calculate"],
            paid_until=record["paid_until"]
        )
