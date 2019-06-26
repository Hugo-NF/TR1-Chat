from socket import *
from threading import Thread
import re
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from src.client_ui import ClientWindow, Ui_MainWindow
from src.connect_ui import Ui_connectionDialog
from src.rooms_ui import Ui_roomsDialog


class Client:
    """Handles the communication with the server application"""

    buffer_size = 1024

    def __init__(self, main_ui, rooms_ui, conn_ui):
        """
        Initializes the client side application with UI objects
        :param main_ui: Qt UI object of the main window (principal)
        :param rooms_ui: Qt UI object of the rooms window (Rooms list, creation and switching)
        :param conn_ui: Qt UI object of the connection window (Server connection and nickname choosing)
        """
        # Set UI objects
        self.main_ui = main_ui
        self.rooms_ui = rooms_ui
        self.conn_ui = conn_ui

        # Online servers list
        self.servers = []

        # Regexp to handle server answer
        self.answers_regexp = re.compile("^\\\(insert|quit|rooms|online|server|join|leave|create|servers)=(.*)$")

        # UI initial state
        # Bind send button to send message
        self.main_ui.sendButton.clicked.connect(self.send_action)
        # Send button initiates disabled
        self.main_ui.sendButton.setDisabled(True)
        # Refresh button initiates disabled
        self.main_ui.refreshButton.setDisabled(True)
        # Rooms button initiates hidden
        self.main_ui.roomsButton.hide()
        # Connection progress bar initiates hidden
        self.conn_ui.connectionProgress.hide()
        # Bind connect button to connect with server
        self.conn_ui.connectButton.clicked.connect(lambda: self.connect(self.conn_ui.hostEdit.text(),
                                                                        self.conn_ui.portEdit.text()))
        # Bind submit button to send nickname
        self.conn_ui.submitButton.clicked.connect(lambda: self.create_user(self.conn_ui.nicknameEdit.text()))
        # Bind create button
        self.rooms_ui.createButton.clicked.connect(self.create_room)
        # Bind join button
        self.rooms_ui.joinButton.clicked.connect(self.join_room)
        # Bind leave button
        self.rooms_ui.leaveButton.clicked.connect(self.leave_room)
        # Leave button initiates
        self.rooms_ui.leaveButton.setDisabled(True)
        # Bind refresh button
        self.rooms_ui.refreshButton.clicked.connect(self.get_rooms)
        # Bind enter button
        self.main_ui.sendEdit.returnPressed.connect(self.send_action)
        # Message box initiates disabled
        self.main_ui.sendEdit.setDisabled(True)
        # Bind refresh button
        self.main_ui.refreshButton.clicked.connect(lambda: self.get_users(self.main_ui.onlineFrame.title()))

    def connect(self, host, port):
        """
        Tries to connect client application with server within host:port
        :param host: IP address of the server
        :param port: Opened port of the server
        """
        # Socket properties
        self.conn_host = host
        self.conn_port = port
        try:
            self.conn_address = (self.conn_host, int(self.conn_port))
            # Creates a socket and tries to connect
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.conn_ui.connectionProgress.show()
            self.socket.connect(self.conn_address)

            # Open box with message to user
            QMessageBox.information(None, 'Connected',
                                    "Successfully connected. Now, please, choose a nice nickname", QMessageBox.Ok)

            # Reconfiguring UI to connected state
            self.conn_ui.connectionProgress.setMaximum(100)
            self.conn_ui.connectionProgress.setValue(100)
            self.conn_ui.connectionProgress.setFormat("Connected")
            self.conn_ui.connectButton.setDisabled(True)
            self.main_ui.connectionButton.setText("Disconnect")
            self.main_ui.connectionButton.clicked.connect(self.disconnect)
            self.conn_ui.nicknameEdit.setDisabled(False)
            self.conn_ui.submitButton.setDisabled(False)

            # Starting a new thread to listen the connection
            self.listening_thread = Thread(target=self.listen)
            self.listening_thread.start()

        # Exceptions to treat user wrong typing mistakes
        except TypeError:
            QMessageBox.warning(None, 'Error', "Check your HOST:PORT configuration",
                                QMessageBox.Ok)
        except ValueError:
            QMessageBox.warning(None, 'Error', "Check your HOST:PORT configuration",
                                QMessageBox.Ok)
        except OSError:
            QMessageBox.critical(None, 'Error', "Could not find a server at {}:{}"
                                 .format(self.conn_host, self.conn_port), QMessageBox.Ok)
            self.conn_ui.connectionProgress.hide()

    def disconnect(self):
        """Shutdown current server connection"""
        # Send message to server to quit appropriately
        self.socket.send(bytes("\\quit", "utf8"))

        # Joining listening thread
        if self.listening_thread.isAlive():
            self.listening_thread.join(1)

        # Close socket connection
        self.socket.shutdown(2)
        self.socket.close()

        # Reconfiguring UI to disconnected state
        self.rooms_ui.leaveButton.setDisabled(True)
        self.rooms_ui.joinButton.setDisabled(False)
        self.main_ui.sendButton.setDisabled(True)
        self.main_ui.refreshButton.setDisabled(True)
        self.main_ui.sendEdit.setDisabled(True)
        self.main_ui.onlineFrame.setTitle("Online")
        self.main_ui.online_clear()
        self.main_ui.connectionButton.setText("Connection")
        self.main_ui.sendButton.setDisabled(True)
        self.main_ui.connectionButton.clicked.disconnect(self.disconnect)
        self.conn_ui.connectionProgress.setMaximum(0)
        self.conn_ui.connectionProgress.setValue(-1)
        self.conn_ui.connectionProgress.hide()
        self.conn_ui.connectButton.setDisabled(False)
        self.conn_ui.nicknameEdit.setDisabled(True)
        self.conn_ui.nicknameEdit.setText("")
        self.conn_ui.submitButton.setDisabled(True)
        self.main_ui.roomsButton.hide()

        # Open box with message to user
        QMessageBox.information(None, 'Disconnected',
                                "Disconnected successfully", QMessageBox.Ok)

    def reconnect(self, host, port):
        # Socket properties
        self.conn_host = host
        self.conn_port = port

        self.conn_address = (self.conn_host, int(self.conn_port))
        # Creates a socket and tries to connect
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(self.conn_address)

        # Starting a new thread to listen the connection
        self.listening_thread = Thread(target=self.listen)
        self.listening_thread.start()

    def listen(self):
        """Listens for server messages"""
        proceed = True
        while proceed:
            try:
                # Blocking recv socket call
                message = self.socket.recv(self.buffer_size).decode("utf8")
                # Treat message and returns if listening continues or not
                proceed = self.treat_message(message)
            except OSError:  # Client has left
                break
            # TODO check: Colocar a exceção de conexão quebrada, apagar o servidor que você estava conectado da lista e enviar um \reconnect{'nick'} para outro servidor online
            except ConnectionResetError:
                self.socket.sendto(bytes("\\reconnect{address}".format(address=(self.conn_host, self.conn_port)), "utf8"),
                                          (self.servers[0].host, self.servers[0].port))
                self.reconnect(self.servers[0].host, self.servers[0].port)


    def send_action(self):
        """
        Grabs the message from UI message box and sends it to the server
        """
        message = self.main_ui.read_message_box()
        self.socket.send(bytes(message, "utf8"))
        # Clears the box to the next message
        self.main_ui.clear_message_box()

    def create_room(self):
        """
        Creates a new room at server
        """
        # Grabs the room name from UI
        room = self.rooms_ui.roomNameEdit.text()
        # User has typed something at text box
        if room != "":
            # Clears text box to next room creation
            self.rooms_ui.roomNameEdit.setText("")
            # Send request to server
            self.socket.send(bytes("\\create{%s}" % room, "utf8"))

    def create_user(self, nick):
        """
        Creates a new user at server
        :param nick: User's nickname. This param is used in slot binding
        """
        # User has typed something at text box
        if nick != "":
            self.nick = nick
            # Send nick to server
            self.socket.send(bytes("\\insert{%s}" % nick, "utf8"))
            # Reconfigure UI to 'User has a nick' state
            self.conn_ui.nicknameEdit.setDisabled(True)
            self.conn_ui.submitButton.setDisabled(True)
            self.main_ui.roomsButton.show()
            # TODO Enviar um comando \servers para receber uma lista dos servidores online

    def get_rooms(self):
        """
        Send a request to receive the list of available rooms
        """
        self.socket.send(bytes("\\rooms", "utf8"))

    def get_users(self, room):
        """
        Send a request to receive the list of user online in a given room
        :param room: Room name that you wish to see who's online. This param is used in slot binding
        """
        self.socket.send(bytes("\\online{%s}" % room, "utf8"))

    def join_room(self):
        """
        Insert client inside requested room
        """
        # Reads UI
        item = self.rooms_ui.roomsList.currentItem()
        # User has selected a room on the list
        if item is not None:
            # Send join request to server
            self.socket.send(bytes("\\join{%s}" % item.text(), "utf8"))

            # Reconfigure UI to 'user has joined a room' state
            self.rooms_ui.leaveButton.setDisabled(False)
            self.rooms_ui.joinButton.setDisabled(True)
            self.main_ui.sendButton.setDisabled(False)
            self.main_ui.sendEdit.setDisabled(False)
            self.main_ui.refreshButton.setDisabled(False)
            self.main_ui.onlineFrame.setTitle(item.text())

        # User didn't selected a room, displays a error message
        else:
            QMessageBox.warning(None, "Joining a room", "You must select a room", QMessageBox.Ok)

    def leave_room(self):
        """
        Removes client from it's current room
        """
        # Send leave request to server
        self.socket.send(bytes("\\leave", "utf8"))

        # Reconfigure UI to 'user has left a room' state
        self.rooms_ui.leaveButton.setDisabled(True)
        self.rooms_ui.joinButton.setDisabled(False)
        self.main_ui.sendButton.setDisabled(True)
        self.main_ui.sendEdit.setDisabled(True)
        self.main_ui.refreshButton.setDisabled(True)
        self.main_ui.onlineFrame.setTitle("Online")
        self.main_ui.online_clear()

    def treat_message(self, message):
        """
        Decides what to do based on message received from server
        :param message: message retrieved from socket
        :return: boolean to stop listening thread or not
        """
        # In the beginning, we expect to continue running
        answer = True
        # Regexp match message
        match = self.answers_regexp.match(message)
        # If match occurred, server has sent a special answer
        if match:
            command, answer = match.groups()
            # Reply to issued insert command
            if command == "insert":
                if answer == "not_valid_nickname":
                    # Reconfiguring UI to 'user doesn't have a nickname' state
                    self.conn_ui.nicknameEdit.setDisabled(False)
                    self.conn_ui.submitButton.setDisabled(False)
                    self.main_ui.roomsButton.hide()

                    # Write message to user at chat box
                    self.main_ui.write_message("[Concord][Login]: Nickname not valid")
            # Reply to issued quit command
            elif command == "quit":
                if answer == "success":
                    # Stop thread
                    answer = False

            # Reply to issued rooms command
            elif command == "rooms":
                # Clears the list
                self.rooms_ui.clear_rooms()
                # Iterates though names and add to list
                for room in answer.split("|"):
                    self.rooms_ui.add_room(room)

            # Reply to issued online command
            elif command == "online":
                # User requested invalid room
                if answer == "no_room":
                    # Write message to user at chat box
                    self.main_ui.write_message("[Concord][Online list]: You must specify a valid room")
                else:
                    # Clears the list
                    self.main_ui.online_clear()
                    # Iterates through names and add to list
                    for user in answer.split("|"):
                        self.main_ui.online_add(user)

            # Reply to user unauthorized action (UI should not permit this, but manual commands still available)
            elif command == "server":
                if answer == "no_room":
                    # Write message to user at chat box
                    self.main_ui.write_message("[Concord][Join]: You must join a room a room first")

            # Reply to issued join command
            elif command == "join":
                # User request invalid room (for example, user clicked join button with outdated rooms list)
                if answer == "failure":
                    # Reconfigure UI to 'user is not in a room' state
                    self.rooms_ui.leaveButton.setDisabled(True)
                    self.rooms_ui.joinButton.setDisabled(False)
                    self.main_ui.sendButton.setDisabled(True)
                    self.main_ui.sendEdit.setDisabled(True)
                    self.main_ui.onlineFrame.setTitle("Online")
                    # Write message to user at chat box
                    self.main_ui.write_message("[Concord][Join]: Room doesn't exists")

            # Reply to issued leave command
            elif command == "leave":
                # User tried to leave without being in a room at first
                if answer == "no_room":
                    # Reconfigure UI to 'user is not in a room' state
                    self.rooms_ui.leaveButton.setDisabled(True)
                    self.rooms_ui.joinButton.setDisabled(False)
                    self.main_ui.sendButton.setDisabled(True)
                    self.main_ui.sendEdit.setDisabled(True)
                    self.main_ui.onlineFrame.setTitle("Online")
                    # Write message to user at chat box
                    self.main_ui.write_message("[Concord][Leave]: You're not in a room")

            # Reply to issued create command
            elif command == "create":
                # Room successfully created
                if answer == "success":
                    # Write message to user at chat box
                    self.main_ui.write_message("[Concord][Create]: Room successfully created")

                # User tried to recreate a room
                elif answer == "failure":
                    # Write message to user at chat box
                    self.main_ui.write_message("[Concord][Create]: Room already exists")

            # TODO Passar a aceitar a resposta do comando \servers, onde vocês vão criar a lista de servidores
            # TODO Se já houver uma, apague e crie uma mais atualizada com base no comando mais atual

        # Message didn't matched with regexp, just print it on screen
        else:
            self.main_ui.write_message(message)
        # return boolean
        return answer


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Concord")
    app.setApplicationName("Concord")

    main_window = ClientWindow()
    conn_dialog = QDialog(main_window)
    rooms_dialog = QDialog(main_window)

    main_ui = Ui_MainWindow()
    conn_ui = Ui_connectionDialog()
    rooms_ui = Ui_roomsDialog()

    # Draw the window
    main_ui.setupUi(main_window)
    conn_ui.setupUi(conn_dialog)
    rooms_ui.setupUi(rooms_dialog)

    # Initialize client
    client = Client(main_ui, rooms_ui, conn_ui)

    # Application initial configuration
    main_ui.connectionButton.clicked.connect(conn_dialog.show)
    main_ui.roomsButton.clicked.connect(rooms_dialog.show)

    # Application initial size
    main_window.resize(917, 437)
    main_window.setFixedSize(917, 437)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())
