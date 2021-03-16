import socket
import sys
import urllib
from kivy.network.urlrequest import UrlRequest
from kivy.support import install_twisted_reactor


# ========================================== SERVER =====================================================

# STACK OVER FLOW REFERENCE
# def Main():
#     host = '127.0.0.1'
#     port = 7000
#
#     mySocket = socket.socket()
#     mySocket.bind((host, port))
#
#     mySocket.listen(1)
#     conn, address = mySocket.accept()
#     print("Connection: " + str(address))
#     message = 'Connected'
#     conn.send(message.encode())
#
#     while True:
#         data = conn.recv(1024).decode()
#         strdata = str(data)
#         print(strdata)
#         reply = 'confirmed'
#         conn.send(reply.encode())
#
#     mySocket.close()
#
#
# if __name__ == '__main__':
#     Main()
#

class Server:
    """
    Class with functions relating to playing online
    """

    def __init__(self, port=700):
        self.address = (socket.gethostname(), port)
        self.socket = socket.socket()
        self.socket.bind(self.address)
        self.players = []
        self.ships = []
        self.coords = None

    def listen(self):
        self.socket.listen()
        client = self.socket.accept()

        message = client[0].recv(1024).decode()
        query = message.rsplit(sep='|')  # rsplit returns a list of the words in the string with a delimiter
        if query[0] == 'ships':
            print('Ships: %s' % query[1])
            self.ships.append(query[1])
            client[0].send(str(len(self.ships) % 2).encode())

        if query[0] == 'coords':
            if not self.coords:
                print('Coords: %s' % query[1])
                self.coords = query[1]
            client[0].send(str(self.coords).encode())

        if query[0] == 'get_coords':
            print('Sending coords: %s' % self.coords)
            client[0].send(str(self.coords).encode())
            self.coords = None

        if query[0] == 'get_player':
            print('Requested player name')
            print(len(self.players))
            if len(self.players) - 1 >= int(query[1]):
                client[0].send(self.players[int(query[1])].encode())
                print(self.players[int(query[1])])
            else:
                client[0].send(str(None).encode())

        if query[0] == 'get_ships':
            print('Requested ships')
            if len(self.ships) - 1 >= int(query[1]):
                client[0].send(self.ships[int(query[1])].encode())
            else:
                client[0].send(str(None).encode())

        if query[0] == 'player':
            print('Sailor: %s' % query[1])
            self.players.append(query[1])
            client[0].send(str(len(self.players) % 2).encode())

    def close(self):
        if self.socket:
            self.socket.close()

# if __name__ == '__main__':
#     Main()
