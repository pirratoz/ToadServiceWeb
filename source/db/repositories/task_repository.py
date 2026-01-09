from datetime import datetime, timezone

from asyncpg import Connection

from source.db.repositories.base_repository import BaseRepository
from source.dto import TaskInfoList


class TaskRepository(BaseRepository):
    def __init__(self, connection: Connection):
        super().__init__(connection)

    async def create_tasks(self, user_id: int) -> None:
        sql = """
        INSERT INTO tasks (user_id, task_type, next_run, turn, extra) VALUES
            ($1, 'work', $2, FALSE, '{"type": null}'),
            ($1, 'reward_clan', $2, FALSE, '{}'),
            ($1, 'reward_marriage', $2, FALSE, '{}'),
            ($1, 'eat_frog', $2, FALSE, '{}'),
            ($1, 'eat_toad', $2, FALSE, '{}');
        """
        await self.connection.execute(sql, user_id, datetime.now(timezone.utc))

    async def get_all_tasks_for_user(self, user_id: int) -> TaskInfoList:
        sql = "SELECT user_id, task_type, next_run, turn, extra FROM tasks WHERE user_id = $1"
        records = await self.connection.fetch(sql, user_id)
        return TaskInfoList.load_from_records(records)
