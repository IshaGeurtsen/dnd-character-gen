from http.server import HTTPServer
from typing import NoReturn
from pathlib import Path

from app.http_server import run, Handler


def main() -> NoReturn:
    run(
        server_class=HTTPServer,
        handler_class=Handler,
        cwd=Path(__file__).parent,
    )


if __name__ == "__main__":
    main()
