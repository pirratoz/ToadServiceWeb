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
from toad_bot.storage import AuthInfoClass
from toad_bot.enums import AuthInfoEnum


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
            "api_id": [int(data.get("api_id", None)) if data.get("api_id", None) else None, user_repo.update_api_id],
            "api_hash": [data.get("api_hash", None), user_repo.update_api_hash],
            "password": [data.get("password", None), user_repo.update_password_2fa],
            "phone": [data.get("phone", None), user_repo.update_phone],
        }
        for key, value in new_data.items():
            if not value[0]:
                continue
            info = await value[1](request.ctx.user_id, value[0])

    return json({"info": info.dump()})

@ajax_page.post("/bot/turn")
@jwt_auth_required
async def set_telegram_turn(request: Request):
    data = request.json

    running = False
    message = ""
    message_type = "info"

    async with request.app.ctx.db_pool.acquire() as connection:
        user_repo = UserRepository(connection)
        user = await user_repo.get_user_by_id(request.ctx.user_id)

        if not user.api_id:
            message_type = "warning"
            message += "Установите - API ID\n"
        
        if not user.api_hash:
            message_type = "warning"
            message += "Установите - API HASH\n"

        if not user.phone:
            message_type = "warning"
            message += "Установите - PHONE\n"

    """
    {
        running: true|false,
        message: "текст",
        message_type: "success|error|warning|info"
    }
    """

    if message_type == "info":
        client = AuthInfoClass.get_client(request.ctx.user_id)
        if client and client.is_connected:
            await client.disconnect()
            message_type = "success"
            message = "Бот остановлен!"
        else:
            client = AuthInfoClass.add_client(
                user_id=request.ctx.user_id,
                api_id=user.api_id,
                api_hash=user.api_hash,
                password_2fa=str(user.password_2fa),
                phone=user.phone
            )
            status = await AuthInfoClass.is_auth(request.ctx.user_id)
            if status == AuthInfoEnum.CLIENT_AUTH_SUCCSESS:
                message_type = "success"
                message = "Бот запущен!"
                running = True
            else:
                status = await AuthInfoClass.auth_send_key(request.ctx.user_id)
                if status == AuthInfoEnum.CLIENT_AUTH_SEND_CODE:
                    message = "Введите код из Telegram!"
                else:
                    message = "Неизвестная ошибка при получении ключа!"
                    message_type = "warning"

    return json(
        {
            "running": running,
            "message": message,
            "message_type": message_type
        }
    )

@ajax_page.post("/bot/code")
@jwt_auth_required
async def set_telegram_code(request: Request):
    data = request.json

    running = False
    message = ""
    message_type = "info"

    server_data = {
        "running": running,
        "message": message,
        "message_type": message_type
    }

    client = AuthInfoClass.get_client(request.ctx.user_id)

    if not client:
        message += "Вы не запустили бота\n"
        message_type = "warning"
        return json(server_data)
    
    hash_code = AuthInfoClass.get_hash_code(request.ctx.user_id)
    
    if not hash_code:
        message += "Хэш не найден, попробуйте запустить бота снова!"
        message_type = "warning"
        return json(server_data)
    
    status = await AuthInfoClass.auth_code(request.ctx.user_id, data["code"])

    if status == AuthInfoEnum.CLIENT_AUTH_SUCCSESS:
        message = "Бот запущен!"
        message_type = "success"
        running = True
    elif status == AuthInfoEnum.CLIENT_PHONE_CODE_EXPIRED:
        message = "Код просрочен, перезапустите бота!"
        message_type = "warning"
    elif status == AuthInfoEnum.CLIENT_PASSWORD_INVALID:
        message = "2fa пароль - неверный"
        message_type = "warning"
    else:
        message = "Произошла ошибка, попробуйте ещё раз или сообщите админу"
        message_type = "warning"

    return json(
        {
            "running": running,
            "message": message,
            "message_type": message_type
        }
    )