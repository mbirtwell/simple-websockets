from os.path import dirname

import static
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request

from websockets.uwsgi import WebSocket

def web_socket_handler(websocket):
    while True:
        msg = websocket.read_message()
        websocket.send_message("Pong from uwsgi: " + msg)


url_map = Map([
    Rule('/', endpoint='static'),
    Rule('/test_path', endpoint='pong_server')
])

web_socket_application = WebSocket.make_application(web_socket_handler)
static_application = static.Cling(dirname(__file__))

@Request.application
def application(request):
    try:
        adapter = url_map.bind_to_environ(request.environ)
        endpoint, args = adapter.match()
        if endpoint == 'pong_server':
            return web_socket_application
        else:
            return static_application
    except HTTPException as exc:
        return exc
