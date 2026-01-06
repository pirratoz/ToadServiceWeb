from source.app.web import get_app
from source.endpoints import (
    main_page,
)


def main() -> None:
    app = get_app()
    app.blueprint(main_page)
    app.run(host="127.0.0.1", port=8888, debug=True, single_process=True)


if __name__ == "__main__":
    main()
