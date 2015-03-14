from hashlib import sha1
from base64 import b64encode
import struct


class WebSocketProtocolError(Exception):
    pass


class WebSocketBase(object):
    magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

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
            'Sec-WebSocket-Accept': digest.decode('latin-1'),
        })

    def read_frame(self):

        hdr = self._raw_read(2)
        # bit 0 is fin
        fin = bool(hdr[0] & 0x80)
        # bits 1-3 are reserved
        # bit 4-7 are op code
        op = hdr[0] & 0x0F
        # bit 8 is masked
        masked = bool(hdr[1] & 0x80)
        length = hdr[1] & 0x7F

        if not fin:
            raise NotImplementedError("Not implemented multi-frame messages")
        if not masked:
            raise WebSocketProtocolError("All client requests must be masked")

        if length == 126:
            length = struct.unpack(">H", self._raw_read(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._raw_read(8))[0]
        masks = self._raw_read(4)

        decoded = bytearray()
        for byte in self._raw_read(length):
            decoded.append(byte ^ masks[len(decoded) % 4])

        if op == 0:
            raise WebSocketProtocolError("Unexpected continuation frame")
        elif op == 1:
            return decoded.decode('utf-8')
        elif op == 2:
            return bytes(decoded)
        elif op in range(8, 11):
            raise NotImplementedError("Unimplemented op code")
        else:
            raise WebSocketProtocolError("Unexpeced reserved op")

    def read_message(self):
        message = None
        while message is None:
            message = self.read_frame()
        return message

    def send_message(self, message):
        fin = True
        op = 0x1
        hdr = int(fin) << 7 | op
        self._raw_write(bytes([hdr]))
        message = message.encode('utf-8')
        length = len(message)
        if length <= 125:
            self._raw_write(bytes([length]))
        elif 126 <= length <= 0xFFFF:
            self._raw_write(bytes([126]))
            self._raw_write(struct.pack(">H", length))
        else:
            self._raw_write(bytes([127]))
            self._raw_write(struct.pack(">Q", length))
        self._raw_write(message)
