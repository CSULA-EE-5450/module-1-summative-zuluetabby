import socket
import urllib


class Client:
    """
    Client class for online players.
    """
    def __init__(self, address=('127.0.0.1', 7000)):
        self.server_address = address
        self.socket = socket.socket()
        self.message = None

    def request(self, query, data=''):
        self.connect()
        # Get it as a string, it's encoded so decode after
        self.socket.send((str(query) + '/' + str(data)).encode())
        self.message = self.socket.recv(1024)
        if self.message:
            self.message = self.message.decode()
        return self.message

    def connect(self):
        self.socket.close()
        self.socket = socket.socket()
        self.socket.connect(self.server_address)
