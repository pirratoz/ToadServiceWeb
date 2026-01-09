from sanic import Sanic
import asyncpg

from source.db.connect import get_dsn
from source.endpoints import (
    main_page,
    info_pages,
)
from source.middlewares import (
    jwt_auth_middleware,
)


async def setup_db_pool(app: Sanic):
    app.ctx.db_pool = await asyncpg.create_pool(dsn=get_dsn())


async def close_db_pool(app: Sanic):
    await app.ctx.db_pool.close()


def get_app() -> Sanic:
    app = Sanic(
        name="Toads"
    )
    app.extend(
        config={
            "templating_enable_async": True,
            "templating_path_to_templates": "source/templates/"
        }
    )
    app.static("/static", "source/static")

    app.blueprint(main_page)
    app.blueprint(info_pages)
    app.register_middleware(jwt_auth_middleware, attach_to="request")
    app.register_listener(setup_db_pool, "before_server_start")
    app.register_listener(close_db_pool, "before_server_stop")
    return app
