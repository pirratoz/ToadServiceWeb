from source.usecases.base import BaseUseCase

from source.db.repositories import (
    UserRepository,
    TaskRepository,
)
from source.dto import UserInfo


class CreateUserUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository, task_repo: TaskRepository):
        self.user_repo = user_repo
        self.task_repo = task_repo
    
    async def execute(self, user_id: int) -> UserInfo:
        user = await self.user_repo.get_user_by_id(user_id)
        if user:
            return user
        user = await self.user_repo.create_user(user_id)
        await self.task_repo.create_tasks(user_id)
        return user
