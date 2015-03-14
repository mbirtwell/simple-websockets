from websockets.wsgi import WebSocket


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
            return WebSocket.make_application(endpoint_func,
                                              **endpoint_kwargs)
    return ws_route_