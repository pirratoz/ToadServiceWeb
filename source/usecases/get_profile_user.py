from source.usecases.base import BaseUseCase

from source.db.repositories import (
    UserRepository,
    TaskRepository,
)
from source.dto import (
    UserInfo,
    TaskInfoList,
)


class GetProfileUserUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository, task_repo: TaskRepository):
        self.user_repo = user_repo
        self.task_repo = task_repo
    
    async def execute(self, user_id: int) -> tuple[UserInfo, TaskInfoList]:
        user = await self.user_repo.get_user_by_id(user_id)
        tasks = await self.task_repo.get_all_tasks_for_user(user_id)
        return user, tasks
