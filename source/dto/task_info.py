from datetime import datetime
from dataclasses import dataclass
from typing import Iterable, Any

from asyncpg import Record

from source.db.enums import TaskTypeEnum


@dataclass
class TaskInfo:
    user_id: int
    task_type: TaskTypeEnum
    next_run: datetime
    turn: bool
    extra: dict[Any, Any]

    @staticmethod
    def load_from_record(record: Record) -> "TaskInfo":
        return TaskInfo(
            user_id=record["user_id"],
            task_type=TaskTypeEnum(record["task_type"]),
            next_run=record["next_run"],
            turn=record["turn"],
            extra=record["extra"]
        )

@dataclass
class TaskInfoList:
    tasks: list[TaskInfo]

    @staticmethod
    def load_from_records(records: Iterable[Record]) -> "TaskInfoList":
        return TaskInfoList(
            tasks=[
                TaskInfo.load_from_record(record)
                for record in records
            ]
        )
