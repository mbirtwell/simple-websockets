

class IWebSocket(object):

    def handshake(self):
        raise NotImplementedError()

    def read_message(self):
        raise NotImplementedError()

    def send_message(self, message):
        raise NotImplementedError()
