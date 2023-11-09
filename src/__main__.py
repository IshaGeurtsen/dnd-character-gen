from http.server import HTTPServer
from typing import NoReturn
from pathlib import Path
import sqlite3

from app.http_server import run, Handler

tables = {
    "user": "CREATE TABLE user(id, name)",
}


def create_tables(cwd: Path) -> None:
    db_path = cwd / "data" / "character_database.db"
    connection = sqlite3.Connection(db_path)
    cur = connection.cursor()
    sqlite_master = cur.execute("SELECT name, sql FROM sqlite_master")
    stored_tables = dict(sqlite_master.fetchall())
    for table_name, sql in tables.items():
        if table_name in stored_tables and sql == stored_tables[table_name]:
            continue
        elif table_name in stored_tables and sql != stored_tables[table_name]:
            raise ValueError(f"migration needed for {table_name}")
        else:
            cur.execute(sql)
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
