import hashlib
import hmac
from datetime import (
    datetime,
    timezone,
    timedelta,
)

from sanic import (
    Blueprint,
    Request,
)
from sanic_ext import render
import jwt

from source.db.repositories import (
    UserRepository,
    TaskRepository,
)
from source.usecases import CreateUserUseCase
from source.configs import (
    TgConfig,
    JwtConfig,
)

main_page = Blueprint(
    name="MainPage"
)


@main_page.get("/auth")
async def handler_auth_page(request: Request):
    jwt_config = JwtConfig()
    tg_config = TgConfig()
    if request.args.get("id", None):
        recived_data = {
            "id": request.args.get("id", None),
            "first_name": request.args.get("first_name", None),
            "last_name": request.args.get("last_name", None),
            "username": request.args.get("username", None),
            "photo_url": request.args.get("photo_url", None),
            "auth_date": request.args.get("auth_date", None),
            "hash": request.args.get("hash", None),
        }

        data_copy = {k: v for k, v in recived_data.items() if k != "hash" and v is not None}

        data_string = "\n".join(f"{k}={v}" for k, v in sorted(data_copy.items())).encode("utf-8")

        secret_key = hashlib.sha256(tg_config.token.encode("utf-8")).digest()
        hmac_calculated = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
        if hmac.compare_digest(hmac_calculated, recived_data["hash"]):
            payload = {
                "sub": recived_data["id"],
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=jwt_config.access_token_exp_minutes)
            }
            with open(jwt_config.private_key_path, "r") as fp:
                jwt_token = jwt.encode(payload, fp.read(), algorithm=jwt_config.algorithm)
            async with request.app.ctx.db_pool.acquire() as connection:
                user = await CreateUserUseCase(
                    user_repo=UserRepository(connection),
                    task_repo=TaskRepository(connection)
                ).execute(int(recived_data["id"]))
            response = await render(template_name="authRedirect.html", status=200)
            response.add_cookie("access_token", jwt_token, max_age=jwt_config.access_token_exp_minutes * 60, secure=False)
            return response

    return await render(template_name="infoRegistration.html", status=200)

@main_page.get("/")
async def handler_root_page(request: Request):
    return await render(
        "toadsMain.html", status=200
    )
