"""Example web socket application running on top of werkzeug

Works OK. Werkzeug will put an extra Connection: close header
in to the handshake responses. Tested with IE and Chrome this
gets ignored.
"""

import static
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request

from websockets.wsgi import WebSocket

def web_socket_handler(websocket):
    while True:
        msg = websocket.read_message()
        websocket.send_message("Pong from werkzeug: " + msg)


url_map = Map([
    Rule('/', endpoint='static'),
    Rule('/test_path', endpoint='pong_server')
])

web_socket_application = WebSocket.make_application(web_socket_handler)
static_application = static.Cling('.')

@Request.application
def application(request):
    adapter = url_map.bind_to_environ(request.environ)
    endpoint, args = adapter.match()
    if endpoint == 'pong_server':
        return web_socket_application
    else:
        return static_application

if __name__ == '__main__':
    run_simple('127.0.0.1', 8002, application, threaded=True)
