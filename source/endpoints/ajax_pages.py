from datetime import datetime
from sanic import (
    Blueprint,
    Request,
    json,
)

from source.db.enums import (
    TaskTypeEnum,
    WorkTypeEnum,
)
from source.decorators import jwt_auth_required
from source.db.repositories import (
    UserRepository,
    TaskRepository,
)

ajax_page = Blueprint(
    name="Ajax",
    url_prefix="/ajax"
)


@ajax_page.post("/set/turn")
@jwt_auth_required
async def handler_set_turn(request: Request):
    """
    JSON:
    {
        "settings": ["is_vip", "is_calculate", "work", "reward_clan", "reward_marriage", "eat_frog", "eat_toad", "frog_day"],
        "value": true/false
    }
    """
    data = request.json
    field = data.get("field")
    value = data.get("value")
    async with request.app.ctx.db_pool.acquire() as connection:
        if field == "is_vip":
            info = await UserRepository(connection).update_vip_status(request.ctx.user_id, value)
        elif field == "is_calculate":
            info = await UserRepository(connection).update_calculate_status(request.ctx.user_id, value)
        else:
            info = await TaskRepository(connection).update_turn_for_task(request.ctx.user_id, TaskTypeEnum(field), value)
    return json({"info": info.dump()})


@ajax_page.post("/set/work")
@jwt_auth_required
async def set_work_type(request: Request):
    user_id = request.ctx.user_id
    data = request.json
    work_type = WorkTypeEnum(data.get("type"))

    async with request.app.ctx.db_pool.acquire() as connection:
        info = await TaskRepository(connection).update_work_type(user_id, work_type)

    return json({"info": info.dump()})

@ajax_page.post("/set/next_run")
@jwt_auth_required
async def set_next_run(request: Request):
    data = request.json
    async with request.app.ctx.db_pool.acquire() as connection:
        info = await TaskRepository(connection).update_next_run_for_task(
            user_id = request.ctx.user_id,
            task=TaskTypeEnum(data.get("type")),
            next_run=datetime.fromisoformat(data.get("next_run"))
        )

    return json({"info": info.dump()})


@ajax_page.post("/set/telegram")
@jwt_auth_required
async def set_telegram_info(request: Request):
    data = request.json
    async with request.app.ctx.db_pool.acquire() as connection:
        user_repo = UserRepository(connection)
        new_data = {
            "api_id": [data.get("api_id", None), user_repo.update_api_id],
            "api_hash": [data.get("api_hash", None), user_repo.update_api_hash],
            "password": [data.get("password", None), user_repo.update_password_2fa],
            "phone": [data.get("phone", None), user_repo.update_phone],
        }
        for key, value in new_data.items():
            if not value[0]:
                continue
            info = await value[1](request.ctx.user_id, value[0])

    return json({"info": info.dump()})