from websockets.interface import IWebSocket


class WebSocket(IWebSocket):

    @classmethod
    def make_application(cls, handler, **kwargs):
        def application(environ, start_response):
            ws = cls(environ)
            handler(websocket=ws, **kwargs)
            return []
        return application

    def __init__(self, environ):
        self.environ = environ
        self.ws = environ["wsgi.websocket"]

    def send_message(self, message):
        return self.ws.send(message)

    def read_message(self):
        return self.ws.read_message()
