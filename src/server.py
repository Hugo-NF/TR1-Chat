# Project imports
# Python built-in for sockets programming
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM

# Python built-in for handling threads
from threading import Thread

# Python built-in for pattern matching
import re

class Server:
    """Implements a multi-threaded server for a asynchronous chat application"""

    buffer_size = 1024

    def __init__(self, host, port, isTcp):
        self.clients = {}
        self.rooms = {}
        self.host = host
        self.port = port
        self.own_address = (self.host, self.port)
        self.commands_re = re.compile("^\\\(quit|leave|join|rooms|online|create)(?:\s*{(.*)})?$", re.MULTILINE)

        if isTcp:
            self.socket = socket(AF_INET, SOCK_STREAM)
        else:
            self.socket = socket(AF_INET, SOCK_DGRAM)

        self.listening_thread = Thread(target=self.listen)

    def listen(self):
        """Listen to network and starts the handling of upcoming connections,
        this is the target for dispatcher thread"""

        while True:
            client, client_address = self.socket.accept()
            print("Connection established with {host}:{port}"
                  .format(host=client_address[0], port=client_address[1]))

            self.clients[client_address] = {'rooms': {}, 'connected': None, 'socket': client}
            Thread(target=self.handle_connection,
                   args=(client_address, client, )).start()

    def handle_connection(self, address, socket):
        """Handles a connection with one client, this is the target for each worker thread"""
        message = socket.recv(self.buffer_size)
        message_text = message.decode('UTF-8')

        match = self.commands_re.match(message_text)
        if match:
            print("Placeholder: User issued a command")
        else:
            client_info = self.clients[address]
            client_room = client_info['connected']
            if client_room is None:
                print("Placeholder: User must connected to a room before")
            else:
                print("Placeholder: broadcast message to all users in 'client_room' excepting the sender user")



    def start_server(self):
        """Initiates the server by binding it's address and starting dispatcher thread"""

        # Bind the socket to address. The socket must not already be bound.
        self.socket.bind(self.own_address)

        # Enable a server to accept connections.
        # backlog = 10: is maximum of waiting connections before system starts to refuse new connections.
        self.socket.listen(10)

        # From now on, we're allowed to receive connections
        print("Server is up and running! Waiting for connections...")
        self.listening_thread.start()
        self.listening_thread.join()
        self.socket.close()