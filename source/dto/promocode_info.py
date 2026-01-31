from dataclasses import dataclass

from asyncpg import Record


@dataclass
class PromocodeInfo:
    id: int
    code: str
    count_activation: int
    duration: str

    @staticmethod
    def load_from_record(record: Record) -> "PromocodeInfo":
        return PromocodeInfo(
            id=record["id"],
            code=record["code"],
            count_activation=record["count_activation"],
            duration=record["duration"]
        )

    def dump(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "count_activation": self.count_activation,
            "duration": self.duration
        }
