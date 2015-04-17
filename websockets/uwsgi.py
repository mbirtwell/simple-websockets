import uwsgi

from websockets.interface import IWebSocket


class WebSocket(IWebSocket):

    @classmethod
    def make_application(cls, handler, **kwargs):
        def application(environ, start_response):
            ws = cls(environ)
            ws.handshake()
            handler(websocket=ws, **kwargs)
            return []
        return application

    def __init__(self, environ):
        self.environ = environ

    def handshake(self):
        uwsgi.websocket_handshake(self.environ['HTTP_SEC_WEBSOCKET_KEY'],
                                  self.environ.get('HTTP_ORIGIN', ''))

    def send_message(self, message):
        return uwsgi.websocket_send(message.encode('utf-8'))

    def read_message(self):
        return uwsgi.websocket_recv().decode('utf-8')

