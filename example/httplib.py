"""Example use of my websocket class with http.server

Integrates nicely with the HTTP server in http.server.
"""
from http.server import SimpleHTTPRequestHandler, HTTPServer, test
from socketserver import ThreadingMixIn
from websockets.httplib import WebSocket


def web_socket_handler(websocket):
    while True:
        msg = websocket.read_message()
        websocket.send_message("Pong: " + msg)


class ExampleWebSocketRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.headers['upgrade'].lower() == 'websocket':
            ws = WebSocket(self)
            ws.handshake()
            web_socket_handler(ws)
        else:
            super().do_GET()

if __name__ == '__main__':
    test(ExampleWebSocketRequestHandler,
         type("ThreadedServer", (ThreadingMixIn, HTTPServer), {}),
         protocol="HTTP/1.1")
