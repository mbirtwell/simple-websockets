from flask import Response
from websockets.wsgi import WebSocket


class AppResponse(Response):
    def __init__(self, app):
        super(AppResponse, self).__init__()
        self._app = app

    def __call__(self, environ, start_response):
        return self._app(environ, start_response)

def ws_route(router, rule, **route_kwargs):
    """ NOTE: This doesn't work with flask see example/flask_exaple.py
    Works much like Flask/Blueprint route except injects a
    websocket key word arg in to the argument list of the
    endpoint.

    :type router: flask.Flask|flask.Blueprint
    """
    def ws_route_(endpoint_func):
        @router.route(rule, **route_kwargs)
        def ws_upgrader(**endpoint_kwargs):
            inner_app = WebSocket.make_application(endpoint_func,
                                              **endpoint_kwargs)
            return AppResponse(inner_app)
    return ws_route_