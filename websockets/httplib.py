from websockets.base import WebSocketBase


class WebSocket(WebSocketBase):

    def __init__(self, request):
        """

        :param request:
        :type request: http.server.BaseHTTPRequestHandler
        :return:
        """
        super(WebSocket, self).__init__()
        self._request = request

    def _get_header(self, key):
        return self._request.headers[key]

    def _do_handshake(self, code, headers):
        request = self._request
        request.log_request(code)
        request.send_response_only(code)
        for k, v in headers.items():
            request.send_header(k, v)
        request.end_headers()

    def _raw_read(self, count):
        return self._request.rfile.read(count)

    def _raw_write(self, data):
        return self._request.wfile.write(data)
