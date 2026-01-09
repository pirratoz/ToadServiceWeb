from sanic import (
    Blueprint,
    Request,
)
from sanic_ext import render

from source.decorators import jwt_auth_required


info_pages = Blueprint(
    name="InfoPages",
    url_prefix="/info"
)


@info_pages.get("/registration")
async def handler_registration_page(request: Request):
    return await render(
        "infoRegistration.html", status=200
    )

@info_pages.get("/profile")
@jwt_auth_required
async def handler_profile_page(request: Request):
    return await render(
        "infoProfile.html", status=200
    )