# Server imports
import traceback
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM     # Socket programming
from threading import Thread                                    # Python Threads
import re                                                       # Regular expressions
import sys                                                      # System calls

# Local classes
from src.database import Database
from PyQt5.QtWidgets import QApplication, QMainWindow           # PyQt framework
from PyQt5 import QtCore
from src.server_ui import Ui_serverWindow                       # Created Qt interfaces


class Server:
    """Implements a multi-threaded server for a asynchronous chat application"""

    # Path to server sqlite3 db (Will be created if doesn't exist)
    db_path = "../db/server"

    # Flag to stop threads
    run = True

    def __init__(self, ui_obj, host="127.0.0.1", port=8080, is_tcp=True, buffer_size=1024, backlog=10):
        # Data management
        self.clients = {}
        self.db_conn = Database(self.db_path)

        # Regexp to easily switch between commands
        self.commands_re = re.compile("^\\\(quit|leave|join|rooms|online|create)(?:\s*{(.*)})?$", re.MULTILINE)

        # Threads
        self.listening_thread = Thread(target=self.listen)
        self.client_threads = []

        # GUI object configuration
        self.ui_obj = ui_obj
        self._translate = QtCore.QCoreApplication.translate
        self.ui_obj.console("Welcome to Concord Server v.0.0.1\n"
                            "This program is under GNU General Public License v3.0\n"
                            "Authors: Hugo Nascimento Fonseca - 16/0008166\n")
        # TODO: Adicionar os nomes dos demais do grupo
        self.ui_obj.runButton.clicked.connect(self.start_server)

    def listen(self):
        """Listen to network and starts the handling of upcoming connections,
        this is the target for dispatcher thread"""

        while self.run:
            client, client_address = self.socket.accept()
            print("Connection established with {host}:{port}"
                  .format(host=client_address[0], port=client_address[1]))

            self.clients[client_address] = {'rooms': {}, 'connected': None, 'socket': client}

            new_thread = Thread(target=self.handle_connection, args=(client_address, client, ))
            self.client_threads.append(new_thread)
            new_thread.start()

        for thread in self.client_threads:
            thread.join(5)


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

        # Setting socket properties
        self.host = self.ui_obj.hostEdit.text()
        self.port = self.ui_obj.portEdit.value()
        self.buffer_size = self.ui_obj.buffEdit.value()
        self.backlog = self.ui_obj.backlogEdit.value()
        self.own_address = (self.host, self.port)
        if self.ui_obj.tcpRadioButton.isChecked():
            self.socket = socket(AF_INET, SOCK_STREAM)
        else:
            self.socket = socket(AF_INET, SOCK_DGRAM)

        # Bind the socket to address. The socket must not already be bound.
        try:
            self.socket.bind(self.own_address)
            # Enable a server to accept connections.
            self.socket.listen(self.backlog)

            self.run = True
            # From now on, we're allowed to receive connections
            self.listening_thread.start()

            # Adjust UI
            self.ui_obj.runButton.setText(self._translate("serverWindow", "Stop"))
            self.ui_obj.runButton.disconnect()
            self.ui_obj.runButton.clicked.connect(self.stop_server)
            self.ui_obj.console("<span style=\" color: #0dd817;\">Server is up and running! Waiting for connections...<br></span>")
        except OSError:
            self.ui_obj.console("<span style=\" color: #ff0000;\">{traceback}</span>"
                                .format(traceback=traceback.format_exc().replace("\n", "<br>")))
            self.ui_obj.console("<span style=\" color: #ff0000;\">Could not start server at address {addr}. "
                                "Check your configuration and try again</span>".format(addr=self.own_address))

    def stop_server(self):
        self.run = False
        self.listening_thread.join(5*len(self.clients))
        self.socket.close()
        self.ui_obj.console("<span style=\" color: #0dd817;\">Server successfully shutdown<br></span>")
        self.ui_obj.runButton.setText(self._translate("serverWindow", "Run"))
        self.ui_obj.runButton.disconnect()
        self.ui_obj.runButton.clicked.connect(self.start_server)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Application name (display at windows and OS process)
    app.setApplicationDisplayName("Concord Server")
    app.setApplicationName("Concord Server")

    main_window = QMainWindow()
    main_ui = Ui_serverWindow()

    # Draw the window
    main_ui.setupUi(main_window)

    # Application initial size
    main_window.resize(1024, 768)

    # Build a server object
    server = Server(main_ui)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())