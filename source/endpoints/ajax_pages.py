from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from sqlite3 import OperationalError

from pyrogram import errors

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
    PromocodesRepository,
)
import toad_bot.storage as storage
from toad_bot.enums import AuthInfoEnum


ajax_page = Blueprint(
    name="Ajax",
    url_prefix="/ajax"
)


class MessageType(Enum):
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class TelegramServerResponse:
    running: bool
    message: str
    message_type: MessageType

    def dump(self) -> dict:
        return {
            "running": self.running,
            "message": self.message,
            "message_type": self.message_type.value
        }

    def set_running(self, value: bool) -> None:
        self.running = value
    
    def set_message(self, value: str) -> None:
        self.message = value
    
    def add_message(self, value: str) -> None:
        self.message += f"\n{value}"
    
    def set_message_type(self, value: MessageType) -> None:
        self.message_type = value
    
    def set_type_and_message(self, _type: MessageType, message: str) -> None:
        self.message_type = _type
        self.message = message

    @staticmethod
    def get_default() -> "TelegramServerResponse":
        return TelegramServerResponse(
            running=False,
            message="Default Message Response",
            message_type=MessageType.INFO
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
        user_id: int = request.ctx.user_id
        user_repo = UserRepository(connection)
        task_repo = TaskRepository(connection)
        if field == "is_vip":
            info = await user_repo.update_vip_status(user_id, value)
        elif field == "is_calculate":
            info = await user_repo.update_calculate_status(user_id, value)
        else:
            info = await task_repo.update_turn_for_task(user_id, TaskTypeEnum(field), value)
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
    user_id = request.ctx.user_id
    data = request.json

    """
    {
        running: true|false,
        message: "текст",
        message_type: "success|error|warning|info"
    }
    """

    response = TelegramServerResponse.get_default()

    async with request.app.ctx.db_pool.acquire() as connection:
        user_repo = UserRepository(connection)
        user = await user_repo.get_user_by_id(user_id)

        if not user.api_id:
            response.add_message("Установите - API ID")
        
        if not user.api_hash:
            response.add_message("Установите - API HASH")

        if not user.phone:
            response.add_message("Установите - PHONE")

        if user.is_banned:
            response.add_message("BAN")
        
        if any([not user.api_id, not user.api_hash, not user.phone, user.is_banned]):
            response.set_message_type(MessageType.WARNING)
    
    response.set_running(storage.AuthInfoClass.get_status_client(user_id))

    if response.message_type != MessageType.INFO:
        return json(response.dump())
    
    client = storage.AuthInfoClass.get_client(user_id)
    if storage.AuthInfoClass.get_status_client(user_id):
        storage.AuthInfoClass.client_running[user_id] = False
        await client.stop(block=True)
        response.set_type_and_message(MessageType.SUCCESS, "Бот остановлен!")
        response.set_running(storage.AuthInfoClass.get_status_client(user_id))
        return json(response.dump())

    def get_client():
        return storage.AuthInfoClass.add_client(
            user_id=user_id,
            api_id=user.api_id,
            api_hash=user.api_hash,
            password_2fa=str(user.password_2fa),
            phone=user.phone
        )
    
    client = get_client()

    try:
        status = await client.is_connected
        print(f"STATUS: {status}")
        if not status:
            await storage.AuthInfoClass.auth_send_key(user_id)
        else:
            await client.start()
        storage.AuthInfoClass.client_running[user_id] = True
        response.set_type_and_message(MessageType.SUCCESS, "Бот запущен!")
        response.set_running(True)
    except errors.Unauthorized as error:
        response.add_message(error)
        storage.AuthInfoClass.remove_files(user_id)
        client = get_client()
        status = await storage.AuthInfoClass.auth_send_key(user_id)
        if status == AuthInfoEnum.CLIENT_AUTH_SEND_CODE:
            response.add_message("Введите код из Telegram!")
        else:
            response.set_type_and_message(MessageType.WARNING, "Неизвестная ошибка при получении ключа!")
    except OperationalError:
        storage.AuthInfoClass.remove_files(user_id)
        response.add_message("Перезагрузите страницу и попробуйте ещё раз")

    return json(response.dump())

@ajax_page.post("/bot/code")
@jwt_auth_required
async def set_telegram_code(request: Request):
    data = request.json

    response = TelegramServerResponse.get_default()

    client = storage.AuthInfoClass.get_client(request.ctx.user_id)

    if not client:
        response.set_type_and_message(MessageType.WARNING, "Вы не запустили бота!")
        response.set_running(storage.AuthInfoClass.get_status_client(request.ctx.user_id))
        return json(response.dump())
    
    async with request.app.ctx.db_pool.acquire() as connection:
        user_repo = UserRepository(connection)
        user = await user_repo.get_user_by_id(request.ctx.user_id)

        if user.is_banned:
            response.set_type_and_message(MessageType.WARNING, "BAN")
            response.set_running(storage.AuthInfoClass.get_status_client(request.ctx.user_id))
            return json(response.dump())

    hash_code = storage.AuthInfoClass.get_hash_code(request.ctx.user_id)
    
    if not hash_code:
        response.set_type_and_message(MessageType.WARNING, "Хэш не найден, попробуйте запустить бота снова!")
        response.set_running(storage.AuthInfoClass.get_status_client(request.ctx.user_id))
        return json(response.dump())
    
    status = await storage.AuthInfoClass.auth_code(request.ctx.user_id, data["code"])

    if status == AuthInfoEnum.CLIENT_AUTH_SUCCSESS:
        response.set_running(False)
        response.set_type_and_message(MessageType.SUCCESS, "Авторизация пройдена!\nНажмите запустить бота!")
    elif status == AuthInfoEnum.CLIENT_PHONE_CODE_EXPIRED:
        response.set_type_and_message(MessageType.WARNING, "Код просрочен, перезапустите бота!")
    elif status == AuthInfoEnum.CLIENT_PASSWORD_INVALID:
        response.set_type_and_message(MessageType.WARNING, "2fa пароль - неверный")
    else:
        response.set_type_and_message(MessageType.WARNING, "Произошла ошибка, попробуйте ещё раз или сообщите админу")

    response.set_running(storage.AuthInfoClass.get_status_client(request.ctx.user_id))

    return json(response.dump())


@ajax_page.post("/code/input")
@jwt_auth_required
async def input_code_user(request: Request):
    data = request.json
    code = data.get("code", "").strip()
    async with request.app.ctx.db_pool.acquire() as connection:
        info = await PromocodesRepository(connection).use_promocode(
            user_id=request.ctx.user_id,
            code=code
        )

    return json(info)
