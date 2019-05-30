# Project imports
# Python built-in for sockets programming
from socket import AF_INET, socket, SOCK_STREAM

# Python build-in for handling threads
from threading import Thread

class Client:
    """Handles the communication with the server application"""

    buffer_size = 1024

    def __init__(self, host, port):
        """Initializes the client side application with a given host and port"""
        self.conn_host = host
        self.conn_port = port
        self.conn_address = (self.conn_host, self.conn_port)
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self.socket.connect(self.conn_address)


client = Client("localhost", 8080)