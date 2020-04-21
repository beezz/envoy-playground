from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import platform
import time

NODE = platform.node()


class OpSelector:

    @staticmethod
    def normal(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(f"{NODE}\n".encode("utf-8")))
        self.wfile.write(bytes("normal\n".encode("utf-8")))

    @staticmethod
    def error(self):
        self.send_response(500)
        self.end_headers()
        self.wfile.write(bytes(f"{NODE}\n".encode("utf-8")))
        self.wfile.write(bytes("error\n".encode("utf-8")))


    @staticmethod
    def notimplemented(self):
        raise NotImplementedError(f"op={self._op} not implemented")

    @staticmethod
    def shutdown(self):
        # prematuraly end a req-resp cycle
        self.server.shutdown_request(self.request)



class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_parsed = urlparse(self.path)
        query_params = parse_qs(url_parsed.query)
        self._op = op = query_params.get("op", ["normal"])[0]
        print(f"op={op}")

        #  IPython.embed()
        getattr(OpSelector, op, OpSelector.notimplemented)(self)

        return


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run(handler_class=HTTPRequestHandler)
