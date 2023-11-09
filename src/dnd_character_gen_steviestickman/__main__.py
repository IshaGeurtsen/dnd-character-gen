from typing import NoReturn
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import sys
from typing import NewType, Any, BinaryIO


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

    def do_GET(self) -> None:
        if "text/html" in self.headers["Accept"]:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf8")
            self.send_header("Content-Length", str(len("<p>hello world</p>")))
            self.end_headers()
            self.flush_headers()
            self.wfile.write(b"<p>hello world</p>")
        else:
            self.send_error(HTTPStatus.NOT_ACCEPTABLE)


def run(
    server_class: type[HTTPServer],
    handler_class: type[BaseHTTPRequestHandler],
    ip: Ip = Ip("localhost"),
    port: Port = Port(8000),
) -> NoReturn:
    server_address = ip, port
    httpd = server_class(server_address, handler_class)
    print(f"listening on https://{ip}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit()


def main() -> NoReturn:
    run(
        server_class=HTTPServer,
        handler_class=Handler,
    )


if __name__ == "__main__":
    main()
