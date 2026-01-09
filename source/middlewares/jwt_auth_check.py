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

    token = request.cookies.get("access_token")
    if not token:
        return redirect("/info/registration")

    try:
        with open(getenv("JWT_PUBLIC_KEY_PATH")) as fp:
            payload = jwt.decode(
                token,
                fp.read(),
                algorithms=[getenv("JWT_ALGORITHM")]
            )
    except jwt.ExpiredSignatureError:
        return redirect("/info/registration")
    except jwt.InvalidTokenError:
        return redirect("/info/registration")

    request.ctx.user_id = payload["sub"]
