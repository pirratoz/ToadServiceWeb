from datetime import datetime, timezone

from asyncpg import Connection

from source.db.repositories.base_repository import BaseRepository
from source.dto import (
    TaskInfoList,
    TaskInfo,
)
from source.db.enums import (
    TaskTypeEnum,
    WorkTypeEnum,
)


class TaskRepository(BaseRepository):
    def __init__(self, connection: Connection):
        super().__init__(connection)

    async def create_tasks(self, user_id: int) -> None:
        sql = """
        INSERT INTO tasks (user_id, task_type, next_run, turn, extra) VALUES
            ($1, 'work', $2, FALSE, '{"type": "carefree"}'),
            ($1, 'reward_clan', $2, FALSE, '{}'),
            ($1, 'reward_marriage', $2, FALSE, '{}'),
            ($1, 'eat_frog', $2, FALSE, '{}'),
            ($1, 'eat_toad', $2, FALSE, '{}'),
            ($1, 'frog_day', $2, FALSE, '{}');
        """
        await self.connection.execute(sql, user_id, datetime.now(timezone.utc))

    async def get_all_tasks_for_user(self, user_id: int) -> TaskInfoList:
        sql = "SELECT user_id, task_type, next_run, turn, extra FROM tasks WHERE user_id = $1"
        records = await self.connection.fetch(sql, user_id)
        return TaskInfoList.load_from_records(records)

    async def update_turn_for_task(self, user_id: int, task: TaskTypeEnum, turn: bool) -> TaskInfo:
        record = await self.connection.fetchrow(
            """
            UPDATE tasks
            SET turn = $1
            WHERE user_id = $2 AND task_type = $3
            RETURNING *
            """,
            turn,
            user_id,
            task.value
        )
        return TaskInfo.load_from_record(record)

    async def update_work_type(self, user_id: int, type: WorkTypeEnum) -> TaskInfo:
        sql = """
        UPDATE tasks
        SET extra = jsonb_set(
            COALESCE(extra, '{}'::jsonb),
            '{type}',
            to_jsonb($1::text),
            true
        )
        WHERE user_id = $2 AND task_type = $3
        RETURNING *
        """
        record = await self.connection.fetchrow(
            sql,
            type.value,
            user_id,
            TaskTypeEnum.WORK.value
        )
        return TaskInfo.load_from_record(record)

    async def update_next_run_for_task(
        self, 
        user_id: int, 
        task: TaskTypeEnum, 
        next_run: datetime
    ) -> TaskInfo:
        record = await self.connection.fetchrow(
            """
            UPDATE tasks
            SET next_run = $1
            WHERE user_id = $2 AND task_type = $3
            RETURNING *
            """,
            next_run,
            user_id,
            task.value
        )
        return TaskInfo.load_from_record(record)
