from source.app.web import get_app
from dotenv import load_dotenv

import toad_bot.storage.config as config_toad
from toad_bot.api.web_api import WebApi

def main() -> None:
    load_dotenv()
    config_toad.WEB_API = WebApi()
    app = get_app()
    app.run(host="127.0.0.1", port=8888, debug=True, single_process=True)


if __name__ == "__main__":
    main()
