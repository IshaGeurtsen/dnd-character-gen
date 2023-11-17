from http.server import HTTPServer
from typing import NoReturn
from pathlib import Path
import sqlite3

from app.http_server import run, Handler


def create_tables(cwd: Path) -> None:
    db_path = cwd / "data" / "character_database.db"
    connection = sqlite3.Connection(db_path)
    cur = connection.cursor()
    script = cwd / "src" / "create_tables.sql"
    cur.executescript(script.read_text())
    connection.commit()


def main() -> NoReturn:
    create_tables(Path.cwd())
    run(
        server_class=HTTPServer,
        handler_class=Handler,
        cwd=Path.cwd(),
    )


if __name__ == "__main__":
    main()
