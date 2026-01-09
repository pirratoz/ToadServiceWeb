import hashlib
import hmac
from os import getenv
from datetime import (
    datetime,
    timezone,
    timedelta,
)

from sanic import (
    Blueprint,
    Request,
    redirect,
)
from sanic_ext import render
import jwt

from source.db.repositories import UserRepository


main_page = Blueprint(
    name="MainPage"
)


@main_page.get("/auth")
async def handler_auth_page(request: Request):
    if request.args.get("id", None):
        recived_data = {
            "id": request.args.get("id", None),
            "first_name": request.args.get("first_name", None),
            "last_name": request.args.get("last_name", None),
            "username": request.args.get("username", None),
            "photo_url": request.args.get("photo_url", None),
            "auth_date": request.args.get("auth_date", None),
            "hash": request.args.get("hash", None)
        }

        data_copy = {k: v for k, v in recived_data.items() if k != "hash" and v is not None}

        data_string = "\n".join(f"{k}={v}" for k, v in sorted(data_copy.items())).encode("utf-8")

        secret_key = hashlib.sha256(getenv("TG_TOKEN").encode("utf-8")).digest()
        hmac_calculated = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
        if hmac.compare_digest(hmac_calculated, recived_data["hash"]):
            payload = {
                "sub": int(recived_data["id"]),
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=int(getenv("JWT_ACCESS_TOKEN_EXP_MINUTES")))
            }
            with open(getenv("JWT_PRIVATE_KEY_PATH"), "r") as fp:
                jwt_token = jwt.encode(payload, fp.read(), algorithm=getenv("JWT_ALGORITHM"))
            async with request.app.ctx.db_pool.acquire() as connection:
                user_repository = UserRepository(connection)
                user = await user_repository.get_user_by_id(int(recived_data["id"]))
                if not user:
                    user = user_repository.create_user(int(recived_data["id"]))
            response = redirect(to="/info/profile")
            response.add_cookie("access_token", jwt_token, max_age=int(getenv("JWT_ACCESS_TOKEN_EXP_MINUTES")) * 60, secure=False)
            return response

    return await render(
        "web.html", status=200
    )

@main_page.get("/")
async def handler_root_page(request: Request):
    return await render(
        "toadsMain.html", status=200
    )
