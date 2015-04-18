
def get_impl_for_wsgi_server(server_name):
    if server_name == 'uwsgi':
        from .uwsgi import WebSocket
    elif server_name == 'gevent':
        from .gevent import WebSocket
    elif server_name in ['werkzeug', 'wsgiref']:
        from .wsgi import WebSocket
        if server_name == 'wsgiref':
            WebSocket.patch_wsgiref_server()
    else:
        raise ValueError('Unknown wsgi server "{}"'.format(server_name))
    return WebSocket