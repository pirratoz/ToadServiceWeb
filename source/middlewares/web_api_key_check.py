from sanic import (
    Request,
    json,
)

from source.configs import WebConfig


async def web_api_key_auth_middleware(request: Request):
    route = request.route
    if route is None:
        return

    handler = route.handler
    if not getattr(handler, "__web_api_key_auth_required__", False):
        return 

    web_api_key = request.headers.get("Web-API-Key")

    if not web_api_key or web_api_key != WebConfig().api_key:
        return json({"status": "ok"})
    