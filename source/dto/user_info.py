from datetime import datetime
from dataclasses import dataclass
from copy import deepcopy

from asyncpg import Record


@dataclass
class UserInfo:
    id: int
    is_banned: bool
    is_vip: bool
    is_calculate: bool
    paid_until: datetime
    chat_id: int | None
    chat_title: str | None
    api_id: int | None
    api_hash: str | None
    phone: str | None
    password_2fa: str | None

    @staticmethod
    def load_from_record(record: Record) -> "UserInfo":
        return UserInfo(
            id=record["id"],
            is_banned=record["is_banned"],
            is_vip=record["is_vip"],
            is_calculate=record["is_calculate"],
            paid_until=record["paid_until"],
            chat_id=record["chat_id"],
            chat_title=record["chat_title"],
            api_id=record["api_id"],
            api_hash=record["api_hash"],
            phone=record["phone"],
            password_2fa=record["password_2fa"]
        )

    def dump(self, safe: bool | None = None) -> dict:
        """
        safe: default = True
        """
        if safe is None:
            safe = True
        user = self.safe_user() if safe else self
        return {
            "id": user.id,
            "is_banned": user.is_banned,
            "is_vip": user.is_vip,
            "is_calculate": user.is_calculate,
            "paid_until": user.paid_until.isoformat(),
            "chat_id": user.chat_id,
            "chat_title": user.chat_title,
            "api_id": user.api_id,
            "api_hash": user.api_hash,
            "phone": user.phone,
            "password_2fa": user.password_2fa
        }
    
    def safe_user(self) -> "UserInfo":
        user = deepcopy(self)
        user.api_hash = f"{self.api_hash[:4]}{'*' * 12}{self.api_hash[-4:]}" if self.api_hash else None
        user.phone = f"{self.phone[:4]}{'*' * len(self.phone[4:-2])}{self.phone[-2:]}" if self.phone else None
        user.password_2fa = "*" * len(self.password_2fa) if self.password_2fa else None
        return user
