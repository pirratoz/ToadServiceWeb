from sanic import Sanic
import asyncpg
from datetime import (
    datetime,
    timezone,
)

from source.db.connect import get_dsn
from source.endpoints import (
    main_page,
    info_pages,
    ajax_page,
    api_page,
)
from source.middlewares import (
    jwt_auth_middleware,
)
from source.utils import MAPPER_WORK_TOAD


async def setup_db_pool(app: Sanic):
    app.ctx.db_pool = await asyncpg.create_pool(dsn=get_dsn())


async def close_db_pool(app: Sanic):
    await app.ctx.db_pool.close()


def get_app() -> Sanic:
    templating_path_to_templates = "source/templates/"
    app = Sanic(
        name="Toads"
    )
    app.extend(
        config={
            "templating_enable_async": True,
            "templating_path_to_templates": templating_path_to_templates,
        }
    )
    app.static("/static", "source/static")

    app.blueprint(main_page)
    app.blueprint(info_pages)
    app.blueprint(ajax_page)
    app.blueprint(api_page)
    app.register_middleware(jwt_auth_middleware, attach_to="request")
    app.register_listener(setup_db_pool, "before_server_start")
    app.register_listener(close_db_pool, "before_server_stop")

    jinja_env = app.ext.templating.environment
    jinja_env.globals.update(
        {
            "MAPPER_WORK_TOAD": MAPPER_WORK_TOAD,
            "FUNC_CURRENT_TIME_UTC": lambda : datetime.now(timezone.utc),
        }
    )

    return app
