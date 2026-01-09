from os import getenv

from sanic import (
    Request,
    redirect,
)
from sanic.exceptions import Unauthorized
import jwt


async def jwt_auth_middleware(request: Request):
    route = request.route
    if route is None:
        return

    handler = route.handler
    if not getattr(handler, "__auth_required__", False):
        return 

    token: str | None = request.cookies.get("access_token")
    if not token:
        return redirect("/info/registration")

    try:
        with open(file=getenv("JWT_PUBLIC_KEY_PATH"), mode="r") as fp:
            print(token)
            print("===")
            print(fp.read())
            print("===")
            print([getenv("JWT_ALGORITHM")])
            print("===")
            payload = jwt.decode(
                token,
                fp.read(),
                algorithms=[getenv("JWT_ALGORITHM")]
            )
    except jwt.ExpiredSignatureError:
        return redirect("/info/registration")
    except jwt.InvalidTokenError:
        return redirect("/info/registration")

    request.ctx.user_id = int(payload["sub"])
