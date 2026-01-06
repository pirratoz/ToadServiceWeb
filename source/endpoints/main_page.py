from sanic import (
    Blueprint,
    Request,
)
from sanic_ext import render


main_page = Blueprint(
    name="MainPage"
)


@main_page.get("/auth")
async def handler_main_page(request: Request):
    return await render(
        "auth.html", status=200
    )
