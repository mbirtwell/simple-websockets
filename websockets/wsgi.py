import http.client
from websockets.base import WebSocketBase


class WebSocket(WebSocketBase):

    def __init__(self, environ, start_response):
        super(WebSocket, self).__init__()
        self._environ = environ
        self._start_response = start_response
        self._write = None

    def _get_header(self, key):
        return self._environ['HTTP_' + key.upper().replace('-', '_')]

    def _do_handshake(self, code, headers):
        status = "%d %s" % (code, http.client.responses[code])
        self._write = self._start_response(status, list(headers.items()))
        self._write(b"")

    def _raw_read(self, count):
        return self._environ['wsgi.input'].read(count)

    def _raw_write(self, data):
        return self._write(data)

    @classmethod
    def make_application(cls, handler, **kwargs):
        def application(environ, start_response):
            ws = cls(environ, start_response)
            ws.handshake()
            handler(websocket=ws, **kwargs)
            return []
        return application
