from sanic import (
    Blueprint,
    Request,
)
from sanic_ext import render


info_pages = Blueprint(
    name="InfoPages",
    url_prefix="/info"
)


@info_pages.get("/registration")
async def handler_auth_page(request: Request):
    return await render(
        "infoRegistration.html", status=200
    )
