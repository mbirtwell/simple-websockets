from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from os.path import dirname
import static


def websocket_app(environ, start_response):
    if environ["PATH_INFO"] == '/test_path':
        ws = environ["wsgi.websocket"]
        while True:
            message = ws.receive()
            ws.send("Pong from gevent: " + message)

static_application = static.Cling(dirname(__file__))


def application(environ, start_response):
    if environ.get('HTTP_UPGRADE', '').lower() == 'websocket':
        return websocket_app(environ, start_response)
    else:
        return static_application(environ, start_response)

server = pywsgi.WSGIServer(("", 8000), application,
    handler_class=WebSocketHandler)
server.serve_forever()