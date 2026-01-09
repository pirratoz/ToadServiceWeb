from source.app.web import get_app
from source.endpoints import (
    main_page,
    info_pages,
)
from source.middlewares import jwt_auth_middleware
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    app = get_app()
    app.blueprint(main_page)
    app.blueprint(info_pages)
    app.register_middleware(jwt_auth_middleware, attach_to="request")
    app.run(host="127.0.0.1", port=8888, debug=True, single_process=True)


if __name__ == "__main__":
    main()
