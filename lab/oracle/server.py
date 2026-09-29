#!/usr/bin/env python3
"""Same-netns HTTP oracle. Witness proves Gitea dialed this listener."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

WITNESS = b"GITEA-0000-SSRF"


class Handler(BaseHTTPRequestHandler):
    def _reply(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(WITNESS)))
        self.end_headers()
        self.wfile.write(WITNESS)

    def do_GET(self) -> None:  # noqa: N802
        self._reply()

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        self._reply()

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("oracle %s\n" % (fmt % args))


if __name__ == "__main__":
    # 0.0.0.0 so Linux 0.0.0.1 this-host dials land here in the shared netns.
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
