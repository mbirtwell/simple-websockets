"""Example of websockets over wsgi.

Uses the wsgiref WSGI server.

We have a problem here that wsgi says that we shouldn't return
hop-by-hop headers which include Connection and Upgrade. Well
we need to return these to headers or else it just ain't gonna
work so we monkeypatch the wsgiref.util._hoppish function that
checks for this.
See websockets.wsgi.WebSocker.path_wsgiref_server

"""
from six.moves.socketserver import ThreadingMixIn
from wsgiref.simple_server import make_server, WSGIServer

import static

from websockets import get_impl_for_wsgi_server

WebSocket = get_impl_for_wsgi_server('wsgiref')

def web_socket_handler(websocket):
    while True:
        msg = websocket.read_message()
        websocket.send_message("Pong from wsgiref: " + msg)


web_socket_application = WebSocket.make_application(web_socket_handler)
static_application = static.Cling('.')


def application(environ, start_response):
    if environ.get('HTTP_UPGRADE', '').lower() == 'websocket':
        return web_socket_application(environ, start_response)
    else:
        return static_application(environ, start_response)

if __name__ == '__main__':
    make_server(
        '127.0.0.1',
        8001,
        application,
        server_class=type(
            "ThreadedWSGIServer",
            (ThreadingMixIn, WSGIServer, object),
            {})
    ).serve_forever()
