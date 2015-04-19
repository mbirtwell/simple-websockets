

class IWebSocket(object):

    @property
    def closed(self):
        raise NotImplementedError()

    def read_message(self):
        raise NotImplementedError()

    def send_message(self, message):
        raise NotImplementedError()
