from hashlib import sha1
from base64 import b64encode
import unittest
import six

from websockets.base import WebSocketBase


class FakeWebSocket(WebSocketBase):

    def __init__(self, headers, input_data):
        super(FakeWebSocket, self).__init__()
        self.request_headers = headers
        self.input_data = input_data
        self.response_code = None
        self.response_headers = None
        self.sent_data = b""

    def _get_header(self, key):
        return self.request_headers[key]

    def _raw_read(self, count):
        rv = self.input_data[:count]
        self.input_data = self.input_data[count:]
        return rv

    def _raw_write(self, data):
        self.sent_data += data

    def _do_handshake(self, code, headers):
        self.response_code = code
        self.response_headers = headers


class TestHandshake(unittest.TestCase):

    def test_handshake(self):
        example_key = 'dGhlIHNhbXBsZSBub25jZQ=='
        ws = FakeWebSocket({
            'Sec-WebSocket-Key': example_key
        }, "")

        ws.handshake()

        accept_data = (example_key + WebSocketBase.magic).encode('latin-1', 'strict')
        digest = b64encode(sha1(accept_data).digest())
        self.assertEqual(ws.response_code, 101)
        for header_name, header_value in six.iteritems(ws.response_headers):
            self.assertIsInstance(header_name, str)
            self.assertIsInstance(header_value, str)
        self.assertDictEqual(ws.response_headers, {
            'Upgrade': 'websocket',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Accept': str(digest.decode('latin-1')),
        })


class TestReceiveFrame(unittest.TestCase):

    def test_receive_a_short_single_frame_text_message(self):
        # Use a trivial mask key to get started
        ws = FakeWebSocket({}, b"\x81\x85\x00\x00\x00\x00hello")

        frame = ws.read_frame()

        self.assertEqual(frame, "hello")

    def test_receive_a_short_single_frame_text_message_nontrivial_mask_key(self):
        # Use a trivial mask key to get started
        ws = FakeWebSocket({}, b"\x81\x85\x00\xaa\x00\xaah\xcfl\xc6o")

        frame = ws.read_frame()

        self.assertEqual(frame, "hello")

    def test_close_frame_marks_socket_closed(self):
        ws = FakeWebSocket({}, b"\x88\x80\x00\x00\x00\x00")

        self.assertFalse(ws.closed)

        frame = ws.read_frame()

        self.assertIsNone(frame)
        self.assertTrue(ws.closed)


class TestReadMessage(unittest.TestCase):

    def test_recieve_text_message(self):
        ws = FakeWebSocket({}, b"\x81\x85\x00\x00\x00\x00hello")

        frame = ws.read_message()

        self.assertEqual(frame, "hello")

    def test_recieve_close(self):
        ws = FakeWebSocket({}, b"\x88\x80\x00\x00\x00\x00")

        frame = ws.read_message()

        self.assertIsNone(frame)
        self.assertTrue(ws.closed)

class TestSendMessage(unittest.TestCase):

    def test_single_short_text_frame(self):
        ws = FakeWebSocket({}, b"")

        ws.send_message("HELLO")

        self.assertEqual(b"\x81\x05HELLO", ws.sent_data, )
