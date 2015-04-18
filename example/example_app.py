""" Sample generic app

Tested with werkzeug server and uWSGI probably also works with wsgiref.

Werkzeug
See run_werkzeug_server.py for how to launch this with werkzeug.

uWSGI
On the vagrant box defined here this can be started as so (python 3):
WSGI_SERVER=uwsgi bin3/uwsgi --http :8080 --http-websockets --wsgi-file /vagrant/example/example_app.py -p 3
Or as so (python 2):
WSGI_SERVER=uwsgi bin2/uwsgi --http :8080 --http-websockets --wsgi-file /vagrant/example/example_app.py -p 3

GUnicorn + gevent-websocket
Try:
(cd /vagrant/example/ && WSGI_SERVER=gevent gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" example_app:application -b 0.0.0.0:8000)

"""
import os
from os.path import dirname

import static
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request

from websockets import get_impl_for_wsgi_server

server_name = os.environ['WSGI_SERVER']
WebSocket = get_impl_for_wsgi_server(server_name)


def web_socket_handler(websocket):
    while True:
        msg = websocket.read_message()
        websocket.send_message("Pong from {}: {}".format(server_name, msg))


url_map = Map([
    Rule('/', endpoint='static'),
    Rule('/test_path', endpoint='pong_server'),
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
