from hashlib import sha1
from base64 import b64encode
import struct

import six

from websockets.interface import IWebSocket


class WebSocketProtocolError(Exception):
    pass


class WebSocketBase(IWebSocket):

    magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def __init__(self):
        self._closed = False

    @property
    def closed(self):
        return self._closed

    def _get_header(self, key):
        raise NotImplementedError()

    def _do_handshake(self, code, headers):
        raise NotImplementedError()

    def _raw_read(self, count):
        raise NotImplementedError()

    def _raw_write(self, data):
        raise NotImplementedError()

    def handshake(self):
        key = self._get_header('Sec-WebSocket-Key').strip()
        accept_data = (key + self.magic).encode('latin-1', 'strict')
        digest = b64encode(sha1(accept_data).digest())
        self._do_handshake(101, {
            'Upgrade': 'websocket',
            'Connection': 'Upgrade',
            # str and decode required to work in both python 2 and 3
            'Sec-WebSocket-Accept': str(digest.decode('latin-1')),
        })

    def read_frame(self):

        hdr0 = six.byte2int(self._raw_read(1))
        # bit 0 is fin
        fin = bool(hdr0 & 0x80)
        # bits 1-3 are reserved
        # bit 4-7 are op code
        op = hdr0 & 0x0F
        hdr1 = six.byte2int(self._raw_read(1))
        # bit 8 is masked
        masked = bool(hdr1 & 0x80)
        length = hdr1 & 0x7F

        if not fin:
            raise NotImplementedError("Not implemented multi-frame messages")
        if not masked:
            raise WebSocketProtocolError("All client requests must be masked")

        if length == 126:
            length = struct.unpack(">H", self._raw_read(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._raw_read(8))[0]
        masks = list(six.iterbytes(self._raw_read(4)))

        decoded = bytearray()
        for byte in six.iterbytes(self._raw_read(length)):
            decoded.append(byte ^ masks[len(decoded) % 4])

        if op == 0:
            raise WebSocketProtocolError("Unexpected continuation frame")
        elif op == 1:
            return decoded.decode('utf-8')
        elif op == 2:
            return bytes(decoded)
        elif op == 8:
            self._closed = True
            return None
        elif op in range(9, 11):
            raise NotImplementedError("Unimplemented op code")
        else:
            raise WebSocketProtocolError("Unexpeced reserved op")

    def read_message(self):
        message = None
        while message is None and not self.closed:
            message = self.read_frame()
        return message

    def send_message(self, message):
        fin = True
        op = 0x1
        hdr = int(fin) << 7 | op
        self._raw_write(six.int2byte(hdr))
        message = message.encode('utf-8')
        length = len(message)
        if length <= 125:
            self._raw_write(six.int2byte(length))
        elif 126 <= length <= 0xFFFF:
            self._raw_write(six.int2byte(126))
            self._raw_write(struct.pack(">H", length))
        else:
            self._raw_write(six.int2byte(127))
            self._raw_write(struct.pack(">Q", length))
        self._raw_write(message)
