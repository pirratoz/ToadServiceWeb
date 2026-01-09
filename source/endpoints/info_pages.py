from sanic import (
    Blueprint,
    Request,
)
from sanic_ext import render

from source.decorators import jwt_auth_required
from source.db.connect import get_connection
from source.db.repositories import UserRepository


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
    async with request.app.ctx.db_pool.acquire() as connection:
        user = await UserRepository(connection).get_user_by_id(request.ctx.user_id)
    return await render(
        "infoProfile.html", status=200, context={"user": user}
    )