from socket import *                                            # Socket programming
from threading import Thread                                    # Python Threads
import re
import traceback


class Server:
    """Implements a multi-threaded server for a asynchronous chat application"""

    def __init__(self, host="127.0.0.1", port=8080, buffer_size=1024, backlog=10):
        # Data management
        self.clients = {}
        self.rooms = {}

        # Setting socket properties
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.backlog = backlog
        self.own_address = (self.host, self.port)

        # Regexp to easily switch between commands
        self.commands_re = re.compile("^\\\(quit|leave|join|rooms|online|create)(?:\s*{(.*)})?$", re.MULTILINE)

        # Prints a welcome message to console
        print("Welcome to Concord Server v.0.0.1\n"
              "This program is under GNU General Public License v3.0\n")

        # Create TCP socket with user selected properties.
        # setsockopt allows this socket to reuse the same address
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        try:
            # Bind the socket to address.
            # The socket must not already be bound, it may raise the treated OSError exception
            self.socket.bind(self.own_address)
            # Enable a server to accept connections.
            self.socket.listen(self.backlog)

            # Prints console feedback message and reconfigure the buttons
            print("Server is up and running! Waiting for connections...")

            # Set up threads
            self.listening_thread = Thread(target=self.listen)
            self.client_threads = []
            # From now on, we're allowed to receive connections
            self.listening_thread.start()

            # This thread allow us to keep using the terminal
            self.console_thread = Thread(target=self.console)
            self.console_thread.start()

        except OSError:
            # Treating exception thrown by bind
            print(traceback.format_exc())
            print("Check your configuration and try again")

    def stop_server(self):
        """Stops the server by joining all threads and closing the server socket"""
        # TODO Fechar os sockets de todos os clientes

        # Joining all clients threads and clearing threads list
        for thread in self.client_threads:
            if thread.isAlive():
                thread.join(1)
        self.client_threads.clear()

        # Joining listening thread
        if self.listening_thread.isAlive():
            self.listening_thread.join(1)

        # Shutdown and close socket
        self.socket.close()

        # Prints message to console and reconfigure buttons
        print("Server successfully shutdown")

    def listen(self):
        """Listen to network and starts the handling of upcoming connections,
        this is the target for dispatcher thread"""

        while True:
            # Blocking socket call waiting for client connection
            client, client_address = self.socket.accept()

            # Feedback message informing who has just connected
            print("Connection established with {host}:{port}"
                  .format(host=client_address[0], port=client_address[1]))

            # Create a new thread and insert it to server list
            new_thread = Thread(target=self.handle_connection, args=(client_address, client, ))
            self.client_threads.append(new_thread)
            new_thread.start()

    def handle_connection(self, address, socket):
        """
        Handles a connection with one client, this is the target for each worker thread
        Params:
        1. address = tuple with IP (string) and port (integer) of connected user, e.g ('127.0.0.1', 8080)
        2. socket = Python socket object already connected to address

        Description:
        1. Retrieve user's nickname that will be used for entire section
            * New messages will be requested until receiving a unique display name
        2. Starts a 'infinity loop' treating inbound messages from socket
            2.1. Decodes the message between command or chat message
                * If it's a chat message, broadcast it to all users in room
                * If it's a command, execute correspondent action
        """

        # Server console feedback
        print("Thread started for address %s:%s" % (address[0], address[1]))

        # Initial conditions
        proceed = True
        nick = ""
        insert_regexp = re.compile("^\\\(quit|insert)\s*(?:{(.*)})?$", re.MULTILINE)

        try:
            # Loop to get user's nickname
            while proceed:
                # Retrieve message from socket, decode and match with regexp
                message = socket.recv(self.buffer_size)
                message_text = message.decode("utf8")
                match = insert_regexp.match(message_text)

                # If line matched, it means that user issued insert command
                if match:
                    command, nick = match.groups()
                    if command == "quit":
                        socket.send(bytes("\\quit=success", "utf8"))
                        socket.close()
                        print("(Address %s:%s) has quit" % (address[0], address[1]))
                        return
                    elif command == "insert" and nick is not None:
                        if nick in self.clients.keys():
                            socket.send(bytes("\\insert=not_valid_nickname", "utf8"))
                        else:
                            self.clients[nick] = {'address': address, 'socket': socket, 'room': None}
                            proceed = False
                else:
                    socket.send(bytes("\\insert=not_valid_nickname", "utf8"))

            # Server console feedback
            print("Address %s:%s is now using '%s' nickname" % (address[0], address[1], nick))

            # 'Infinity' loop
            while True:
                # Wait until receive a message
                message = socket.recv(self.buffer_size)
                message_text = message.decode("utf8")

                # Tries to match message_text to regexp
                match = self.commands_re.match(message_text)
                if match:
                    command, argument = match.groups()

                    # Quit: broadcast advise to room, send confirmation to client and break outer loop to exit thread
                    if command == 'quit':
                        self.leave_room(nick, socket)
                        del self.clients[nick]
                        socket.send(bytes("\\quit=success", "utf8"))
                        socket.close()
                        print("%s (address %s:%s) has quit" % (nick, address[0], address[1]))
                        return

                    # Rooms: join all keys from rooms hash and send back to user
                    elif command == 'rooms':
                        room_list = "\\rooms=" + "|".join(self.rooms.keys())
                        socket.send(bytes(room_list, "utf8"))

                    # Online: join all keys from rooms['room'] hash and send back to user
                    elif command == 'online':
                        if (argument in self.rooms.keys()) and (argument is not None):
                            users_list = "\\online=" + "|".join(self.rooms[argument]['users'].keys())
                            socket.send(bytes(users_list, "utf8"))
                        else:
                            socket.send(bytes("\\online=no_room", "utf8"))

                    # Join: change 'room' value on user hash entry, add his entry to room,
                    # send confirmation and broadcast message to room
                    elif command == 'join':
                        self.join_room(nick, argument, socket)

                    # Leave: remove his entry from room, clear 'room' value on user hash entry,
                    # send confirmation and broadcast message to room
                    elif command == 'leave':
                        self.leave_room(nick, socket)

                    # Create: create new entry on rooms hash
                    elif command == 'create':
                        self.create_room(argument, socket)

                # The message was a normal text
                else:
                    self.room_announce(message_text, self.clients[nick]['room'], socket, nick)
        except ConnectionResetError:
            if nick != '':
                self.leave_room(nick, socket)
                del self.clients[nick]
            socket.close()
            print("%s (address %s:%s) has quit" % (nick, address[0], address[1]))
            return

    def room_announce(self, msg, room, sender, prefix):
        """Send a message to all sockets given a valid room"""
        # The following condition assumes that rooms_hash will be accessed within function call
        if room is not None:
            Server.broadcast(msg, [client['socket'] for client in self.rooms[room]['users'].values()], prefix)
        else:
            sender.send(bytes("\\server=no_room", "utf8"))

    def join_room(self, user_nick, room, user_socket):
        """Insert user in a room"""
        if (room in self.rooms.keys()) and (room is not None):
            self.clients[user_nick]['room'] = room
            self.rooms[room]['users'][user_nick] = self.clients[user_nick]
            user_socket.send(bytes("\\join=success", "utf8"))
            self.room_announce("{nick} has joined the chat".format(nick=user_nick), room, user_socket, "Server")
            # Server console feedback
            print("'%s' joined '%s' room" % (user_nick, room))
        else:
            # Room does not exist
            user_socket.send(bytes("\\join=failure", "utf8"))

    def leave_room(self, user_nick, user_socket):
        """Remove user from room"""
        if self.clients[user_nick]['room'] is not None:
            user_socket.send(bytes("\\leave=success", "utf8"))
            self.room_announce("{nick} has left the chat".format(nick=user_nick), self.clients[user_nick]['room'], user_socket, "Server")
            del self.rooms[self.clients[user_nick]['room']]['users'][user_nick]
            self.clients[user_nick]['room'] = None

            # Server console feedback
            print("'%s' is now outside of any room" % user_nick)
        else:
            user_socket.send(bytes("\\leave=no_room", "utf8"))

    def create_room(self, room_name, user_socket):
        """Creates a new room"""
        if (room_name not in self.rooms.keys()) and (room_name is not None):
            self.rooms[room_name] = {'users': {}}
            user_socket.send(bytes("\\create=success", "utf8"))

            # Server console feedback
            print("'%s' room has been created" % room_name)
        else:
            # Room already exists
            user_socket.send(bytes("\\create=failure", "utf8"))

    @staticmethod
    def broadcast(msg, recipients, prefix):
        """Static method that sends a message to all socket in recipients list, prefix is for an identification tag"""

        # Prefix is for name identification.
        for recipient in recipients:
            recipient.send(bytes("[{prefix}]: {msg}".format(prefix=prefix, msg=msg), "utf8"))

    def console(self):
        while True:
            command = input()
            if command == "quit":
                self.stop_server()
                break


if __name__ == "__main__":
    # valid = False
    # host, port, buffer_size, backlog = 0, 0, 0, 0
    # while not valid:
    #     try:
    #         host = input("Host (127.0.0.1):")
    #         port = int(input("Port (8080):"))
    #         buffer_size = int(input("Buffer Size (1024):"))
    #         backlog = int(input("Backlog (10):"))
    #         valid = True
    #     except ValueError:
    #         print("Verifique os dados inseridos!")

    server = Server()