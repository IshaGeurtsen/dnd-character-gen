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

    def do_GET(self) -> None:
        parts = self.path.lstrip("/").split("/")
        print(parts, self.path)
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
                try:
                    path = static / "/".join(parts)
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


def run(
    server_class: type[HTTPServer],
    handler_class: type[BaseHTTPRequestHandler],
    cwd: Path,
    ip: Ip = Ip("localhost"),
    port: Port = Port(8000),
) -> NoReturn:
    global static
    static = cwd / "static"
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
