from sanic import (
    Blueprint,
    Request,
    json,
)

from source.db.enums import TaskTypeEnum
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
        "settings": ["vip", "calculate", "work", "reward_clan", "reward_marriage", "eat_frog", "eat_toad", "frog_day"],
        "value": true/false
    }
    """
    data = request.json
    field = data.get("field")
    value = data.get("value")
    async with request.app.ctx.db_pool.acquire() as connection:
        if field == "vip":
            info = await UserRepository(connection).update_vip_status(request.ctx.user_id, value)
        elif field == "calculate":
            info = await UserRepository(connection).update_calculate_status(request.ctx.user_id, value)
        else:
            info = await TaskRepository(connection).update_turn_for_task(request.ctx.user_id, TaskTypeEnum(field), value)
    return json({"info": info.dump()})
