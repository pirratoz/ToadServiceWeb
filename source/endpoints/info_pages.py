from sanic import (
    Blueprint,
    Request,
)
from sanic_ext import render

from source.usecases import GetProfileUserUseCase
from source.decorators import jwt_auth_required
from source.db.repositories import (
    UserRepository,
    TaskRepository,
)


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
        user, tasks = await GetProfileUserUseCase(
            user_repo=UserRepository(connection),
            task_repo=TaskRepository(connection)
        ).execute(request.ctx.user_id)
        user = user.safe_user()
    return await render(
        "infoProfile.html", status=200, context={"user": user, "tasks": tasks}
    )

@info_pages.get("/about")
async def handler_about_page(request: Request):
    return await render(
        "infoAbout.html", status=200
    )