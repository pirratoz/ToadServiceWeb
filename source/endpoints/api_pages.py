from datetime import datetime

from sanic import (
    Blueprint,
    Request,
    json,
)

from source.db.enums import TaskTypeEnum
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


@api_page.post("/tasks/ready")
@web_api_key_required
async def handler_get_ready_tasks(request: Request):
    data = request.json
    user_ids = data["user_ids"]
    if not user_ids:
        return json({"tasks": []})
    async with request.app.ctx.db_pool.acquire() as connection:
        tasks = await TaskRepository(connection).get_ready_task_for_users(user_ids)
    return json(tasks.dump())


@api_page.post("/set/next_run")
@web_api_key_required
async def handler_set_next_run(request: Request):
    # data = {
    #   "user_id": int,
    #   "type": TaskTypeEnum,
    #   "next_run": datetime.isoformat()
    # }
    data = request.json
    async with request.app.ctx.db_pool.acquire() as connection:
        info = await TaskRepository(connection).update_next_run_for_task(
            user_id = data.get("user_id"),
            task=TaskTypeEnum(data.get("type")),
            next_run=datetime.fromisoformat(data.get("next_run"))
        )

    return json({"info": info.dump()})