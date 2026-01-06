from sanic import Sanic


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
    return app

