import socket
#

class Client:

    def __init__(self, address=('127.0.0.0', 0000)):
        self.server_address = address
        self.message = 0
        self.socket = socket.socket()

    def connect(self):
        self.socket.close()
        self.socket = socket.socket()
        self.socket.connect(self.server_address)

    def request(self, query, data=''):
        self.connect()
        self.socket.send(# TODO)
        self.message = self.socket.recv()
        if self.message:
            self.message = self.message.decode()
            return self.message
