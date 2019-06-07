# Server imports
import traceback
from socket import *                                            # Socket programming
from threading import Thread                                    # Python Threads
import re                                                       # Regular expressions
import sys

# Local classes
from PyQt5.QtWidgets import QApplication, QMainWindow           # PyQt framework
from PyQt5 import QtCore
from src.server_ui import Ui_serverWindow, ServerWindow         # Created Qt interfaces


class Server:
    """Implements a multi-threaded server for a asynchronous chat application"""

    # Path to server sqlite3 db (Will be created if doesn't exist)
    db_path = "../db/server"

    def __init__(self, ui_obj, host="127.0.0.1", port=8080, is_tcp=True, buffer_size=1024, backlog=10):
        # Data management
        self.clients = {}
        self.rooms = {}

        # Regexp to easily switch between commands
        self.commands_re = re.compile("^\\\(quit|leave|join|rooms|online|create|insert)(?:\s*{(.*)})?$", re.MULTILINE)

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

        # Create socket with user selected properties.
        # setsockopt allows this socket to reuse the same address
        self.socket = socket(AF_INET, SOCK_STREAM if self.ui_obj.tcpRadioButton.isChecked() else SOCK_DGRAM)
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

            new_thread = Thread(target=self.handle_connection, args=(client_address, client, ))
            self.client_threads.append(new_thread)
            new_thread.start()

    def handle_connection(self, address, socket):
        """Handles a connection with one client, this is the target for each worker thread"""

        proceed = True
        nick = ""
        insert_regexp = re.compile("^\\\insert\s*(?:{(.*)})?$", re.MULTILINE)
        # Getting user nickname
        while proceed:
            message = socket.recv(self.buffer_size)
            message_text = message.decode('UTF-8')
            match = insert_regexp.match(message_text)
            if match:
                nick = match.groups()
                if nick in self.clients.keys():
                    socket.send(bytes("\\server{msg}".format(msg="Nickname already in use"), 'utf8'))
                else:
                    self.clients[nick] = {'address': address, 'socket': socket, 'room': None}
                    proceed = False

        while True:
            message = socket.recv(self.buffer_size)
            message_text = message.decode('UTF-8')

            match = self.commands_re.match(message_text)
            if match:
                command, argument = match.groups()
                if command == 'quit':
                    self.room_announce("{nick} is offline\n".format(nick=nick), self.clients[nick]['room'], None, "Server")
                    socket.send(bytes("\\server{success}", "utf8"))
                    break
                elif command == 'rooms':
                    room_list = "\\rooms = " + "\n".join(self.rooms.keys())
                    socket.send(bytes(room_list, "utf8"))
                elif command == 'online':
                    if (argument in self.rooms.keys()) and (argument is not None):
                        users_list = "\\users = " + "\n".join(self.rooms[argument].keys())
                        socket.send(bytes(users_list, "utf8"))
                elif command == 'join':
                    if (argument in self.rooms.keys()) and (argument is not None):
                        self.clients[nick]['room'] = argument
                        socket.send(bytes("\\server{success}", "utf8"))
                        self.room_announce("{nick} has joined the chat", argument, None, "Server")
                    else:
                        socket.send(bytes("\\server{failure}", "utf8"))
                elif command == 'leave':
                    socket.send(bytes("\\server{success}", "utf8"))
                    self.room_announce("{nick} has left the chat", self.clients[nick]['room'], None, "Server")
                    self.clients[nick]['room'] = None
                elif command == 'create':
                    if (argument not in self.rooms.keys()) and (argument is not None):
                        self.rooms[argument] = {'users': {}}
                        socket.send(bytes("\\server{success}", "utf8"))
                    else:
                        socket.send(bytes("\\server{failure}", "utf8"))
            else:
                self.room_announce(message_text, self.clients[nick]['room'], socket, nick)

    def room_announce(self, msg, room, sender, prefix):
        if room is not None:
            client_list = self.rooms[room]
            Server.broadcast(msg, [client['socket'] for client in client_list.values()], prefix)
        else:
            sender.send(bytes("\\server{noroom}"), "utf8")

    @staticmethod
    def broadcast(msg, recipients, prefix):
        """Broadcasts a message to all the clients."""

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