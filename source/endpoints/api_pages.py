from sanic import (
    Blueprint,
    Request,
    json,
)

from source.decorators import web_api_key_required
from source.usecases import GetProfileUserUseCase
from source.db.repositories import (
    UserRepository,
    TaskRepository,
)

api_page = Blueprint(
    name="Api",
    url_prefix="/api"
)


@api_page.get("/users/<user_id:int>")
@web_api_key_required
async def handler_get_user_info(request: Request, user_id: int):
    async with request.app.ctx.db_pool.acquire() as connection:
        user, tasks = await GetProfileUserUseCase(
            user_repo=UserRepository(connection),
            task_repo=TaskRepository(connection)
        ).execute(user_id)
    return json({
        "user": user.dump(False),
        "tasks": tasks.dump()
    })
