from typing import NoReturn
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
    SimpleHTTPRequestHandler,
)
from http import HTTPStatus
import sys
from typing import NewType, Any, BinaryIO, cast
from pathlib import Path
from os import fspath
from urllib.parse import parse_qs
import sqlite3
from uuid import uuid4

Ip = NewType("Ip", str)
Port = NewType("Port", int)
Address = tuple[Ip, Port]


class Handler(BaseHTTPRequestHandler):
    client_address: Address
    command: Any
    path: str
    version: Any
    rfile: BinaryIO
    wfile: BinaryIO
    protocol_version: str
    extensions_map = SimpleHTTPRequestHandler.extensions_map

    def send_document(
        self,
        code: HTTPStatus,
        mime: str,
        doc: BinaryIO,
    ) -> None:
        binary = doc.read()
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(binary)))
        self.end_headers()
        self.flush_headers()
        self.wfile.write(binary)

    def guess_type(self, path: str) -> str:
        return SimpleHTTPRequestHandler.guess_type(
            cast(SimpleHTTPRequestHandler, self), path
        )

    def redirect(self, code: HTTPStatus, path: str) -> None:
        self.send_response(code)
        self.send_header("Location", path)
        self.end_headers()
        self.flush_headers()

    def do_GET(self) -> None:
        parts = self.path.lstrip("/").split("/")
        match parts:
            case ["dynamic"]:
                raise NotImplementedError
            case ["static", ""]:
                with (static / "index.html").open("rb") as doc:
                    self.send_document(HTTPStatus.OK, "text/html", doc)
            case ["favicon.ico"]:
                with (static / "favicon.png").open("rb") as doc:
                    self.send_document(HTTPStatus.OK, "image/png", doc)
            case ["static", *parts]:
                path = static / "/".join(parts)
                if path.is_dir() and (path / "index.html").is_file():
                    path = path / "index.html"
                try:
                    with path.open("rb") as doc:
                        self.send_document(
                            HTTPStatus.OK,
                            self.guess_type(fspath(path)),
                            doc,
                        )
                except FileNotFoundError:
                    self.log_error(f"could not find {self.path}")
                    self.send_error(HTTPStatus.NOT_FOUND)
            case [""]:
                self.send_response(HTTPStatus.FOUND)
                self.send_header("Location", "/static/")
                self.end_headers()
                self.flush_headers()

    def do_POST(self) -> None:
        if self.path == "/static/user_detail.html":
            self.redirect(HTTPStatus.FOUND, "/static/signin.html")
            data = self.rfile.read(int(self.headers["Content-Length"])).decode(
                encoding="utf-8"
            )
            querry = parse_qs(data)
            with sqlite3.Connection(db) as conn:
                cursor = conn.cursor()
                username = querry["username"][0]
                result = cursor.execute(
                    "SELECT name, id FROM user WHERE name=?", [username]
                )
                value = result.fetchone()
                if value:
                    username, userid = value
                    self.log_message(f"found user {username}, signin in")
                else:
                    userid = uuid4()
                    cursor.execute(
                        "INSERT INTO user (id, name) VALUES (?, ?)",
                        [userid.hex, username],
                    )
                    self.log_message(f"creating user {username}, signin in")
                    conn.commit()


def run(
    server_class: type[HTTPServer],
    handler_class: type[BaseHTTPRequestHandler],
    cwd: Path,
    ip: Ip = Ip("localhost"),
    port: Port = Port(8000),
) -> NoReturn:
    global static, db
    static = cwd / "src" / "static"
    db = cwd / "data" / "character_database.db"
    server_address = ip, port
    httpd = server_class(server_address, handler_class)
    print(f"listening on http://{ip}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit()


static: Path
db: Path
