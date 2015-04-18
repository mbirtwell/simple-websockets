

class IWebSocket(object):

    def read_message(self):
        raise NotImplementedError()

    def send_message(self, message):
        raise NotImplementedError()
