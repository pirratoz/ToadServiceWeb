from datetime import datetime
from dataclasses import dataclass

from asyncpg import Record


@dataclass
class HistoryPromocodeInfo:
    id: int
    user_id: int
    promocode_id: int
    activated_at: datetime

    @staticmethod
    def load_from_record(record: Record) -> "HistoryPromocodeInfo":
        return HistoryPromocodeInfo(
            id=record["id"],
            code=record["code"],
            count_activation=record["count_activation"],
            duration=record["duration"]
        )

    def dump(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "promocode_id": self.promocode_id,
            "activated_at": self.activated_at.isoformat()
        }
