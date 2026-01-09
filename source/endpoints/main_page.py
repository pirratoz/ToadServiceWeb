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
                "sub": recived_data["id"],
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=int(getenv("JWT_ACCESS_TOKEN_EXP_MINUTES")))
            }
            with open(getenv("JWT_PRIVATE_KEY_PATH"), "r") as fp:
                token = jwt.encode(payload, fp.read(), algorithm=getenv("JWT_ALGORITHM"))
            response = redirect(to="/info/registration")
            response.cookies["access_token"] = f"Bearer {token}"
            return response

    return await render(
        "web.html", status=200
    )

@main_page.get("/")
async def handler_root_page(request: Request):
    return await render(
        "toadsMain.html", status=200
    )
