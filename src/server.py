from socket import *                                            # Socket programming
from threading import Thread                                    # Python Threads
import re                                                       # Regular expressions
import sys
import traceback

from PyQt5.QtWidgets import QApplication                        # PyQt framework
from PyQt5 import QtCore
from src.server_ui import Ui_serverWindow, ServerWindow         # Created Qt interfaces


class Server:
    """Implements a multi-threaded server for a asynchronous chat application"""

    def __init__(self, ui_obj, host="127.0.0.1", port=8080, buffer_size=1024, backlog=10):
        # Data management
        self.clients = {}
        self.rooms = {}

        # Regexp to easily switch between commands
        self.commands_re = re.compile("^\\\(quit|leave|join|rooms|online|create)(?:\s*{(.*)})?$", re.MULTILINE)

        # GUI object configuration
        self.ui_obj = ui_obj
        # Translate object to multi-language application (if needed)
        self._translate = QtCore.QCoreApplication.translate
        # Prints a welcome message to console
        self.ui_obj.console("Welcome to Concord Server v.0.0.1\n"
                            "This program is under GNU General Public License v3.0\n")

        # Connects run and stop button to correspondent actions
        self.ui_obj.runButton.clicked.connect(self.start_server)
        self.ui_obj.stopButton.clicked.connect(self.stop_server)
        self.ui_obj.stopButton.setDisabled(True)

    def start_server(self):
        """Initiates the server by binding it's address and starting dispatcher thread"""

        # Setting socket properties
        self.host = self.ui_obj.hostEdit.text()
        self.port = self.ui_obj.portEdit.value()
        self.buffer_size = self.ui_obj.buffEdit.value()
        self.backlog = self.ui_obj.backlogEdit.value()
        self.own_address = (self.host, self.port)

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
            self.ui_obj.console("Server is up and running! Waiting for connections...")
            self.ui_obj.runButton.setDisabled(True)
            self.ui_obj.stopButton.setDisabled(False)

            # Set up threads
            self.listening_thread = Thread(target=self.listen)
            self.client_threads = []
            # From now on, we're allowed to receive connections
            self.listening_thread.start()

        except OSError:
            # Treating exception thrown by bind
            self.ui_obj.console("<span style=\" color: #ff0000;\">{traceback}</span>"
                                .format(traceback=traceback.format_exc().replace("\n", "<br>")))
            self.ui_obj.console("<span style=\" color: #ff0000;\">Could not start server at address {addr}. "
                                "Check your configuration and try again</span>".format(addr=self.own_address))

    def stop_server(self):
        """Stops the server by joining all threads and closing the server socket"""
        # Joining all clients threads and clearing threads list
        for thread in self.client_threads:
            if thread.isAlive():
                thread.join(1)
        self.client_threads.clear()

        # Joining listening thread
        if self.listening_thread.isAlive():
            self.listening_thread.join(1)

        # Shutdown and close socket
        self.socket.shutdown(2)
        self.socket.close()

        # Prints message to console and reconfigure buttons
        self.ui_obj.console("Server successfully shutdown")
        self.ui_obj.runButton.setDisabled(False)
        self.ui_obj.stopButton.setDisabled(True)

    def listen(self):
        """Listen to network and starts the handling of upcoming connections,
        this is the target for dispatcher thread"""

        while True:
            # Blocking socket call waiting for client connection
            client, client_address = self.socket.accept()

            # Feedback message informing who has just connected
            self.ui_obj.console("Connection established with {host}:{port}"
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
        self.ui_obj.console("Thread started for address %s:%s" % (address[0], address[1]))

        # Initial conditions
        proceed = True
        nick = ""
        insert_regexp = re.compile("^\\\(quit|insert)\s*(?:{(.*)})?$", re.MULTILINE)

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
        self.ui_obj.console("Address %s:%s is now using '%s' nickname" % (address[0], address[1], nick))

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
                    self.ui_obj.console("%s (address %s:%s) has quit" % (nick, address[0], address[1]))
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
            self.ui_obj.console("'%s' joined '%s' room" % (user_nick, room))
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
            self.ui_obj.console("'%s' is now outside of any room" % user_nick)
        else:
            user_socket.send(bytes("\\leave=no_room", "utf8"))

    def create_room(self, room_name, user_socket):
        """Creates a new room"""
        if (room_name not in self.rooms.keys()) and (room_name is not None):
            self.rooms[room_name] = {'users': {}}
            user_socket.send(bytes("\\create=success", "utf8"))

            # Server console feedback
            self.ui_obj.console("'%s' room has been created" % room_name)
        else:
            # Room already exists
            user_socket.send(bytes("\\create=failure", "utf8"))

    @staticmethod
    def broadcast(msg, recipients, prefix):
        """Static method that sends a message to all socket in recipients list, prefix is for an identification tag"""

        # Prefix is for name identification.
        for recipient in recipients:
            recipient.send(bytes("[{prefix}]: {msg}".format(prefix=prefix, msg=msg), "utf8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Application name (display at windows and OS process)
    app.setApplicationDisplayName("Concord Server")
    app.setApplicationName("Concord Server")

    main_ui = Ui_serverWindow()
    main_window = ServerWindow()

    # Draw the window
    main_ui.setupUi(main_window)

    # Application initial size
    main_window.resize(1024, 768)

    # Build a server object
    server = Server(main_ui)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())