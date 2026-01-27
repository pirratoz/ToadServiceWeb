import jwt
from sanic import (
    Request,
    redirect,
)

from source.configs import JwtConfig


async def jwt_auth_middleware(request: Request):
    config = JwtConfig()
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
        with open(file=config.public_key_path, mode="r") as fp:
            payload = jwt.decode(
                token,
                fp.read(),
                algorithms=[config.algorithm]
            )
    except jwt.ExpiredSignatureError:
        return redirect("/info/registration")
    except jwt.InvalidTokenError:
        return redirect("/info/registration")

    request.ctx.user_id = int(payload["sub"])
