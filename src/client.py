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
        """Initializes the client side application with UI objects"""
        # UI object
        self.main_ui = main_ui
        self.rooms_ui = rooms_ui
        self.conn_ui = conn_ui
        self.answers_regexp = re.compile("^\\\(insert|quit|rooms|online|server|join|leave|create)=(.*)$")

        self.main_ui.sendButton.clicked.connect(self.send_action)
        self.main_ui.sendButton.setDisabled(True)
        self.main_ui.roomsButton.hide()
        self.rooms_ui.createButton.clicked.connect(self.create_room)
        self.conn_ui.connectionProgress.hide()
        self.conn_ui.connectButton.clicked.connect(lambda: self.connect(self.conn_ui.hostEdit.text(),
                                                                        self.conn_ui.portEdit.text()))
        self.rooms_ui.roomsList.itemDoubleClicked.connect(lambda: self.get_users(
            self.rooms_ui.roomsList.currentItem()))

        self.rooms_ui.joinButton.clicked.connect(self.join_room)
        self.rooms_ui.leaveButton.clicked.connect(self.leave_room)
        self.rooms_ui.leaveButton.setDisabled(True)

    def connect(self, host, port):
        """Tries to connect client application with server within host:port"""
        # Socket properties
        self.conn_host = host
        self.conn_port = port
        try:
            self.conn_address = (self.conn_host, int(self.conn_port))
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.conn_ui.connectionProgress.show()
            self.socket.connect(self.conn_address)

            QMessageBox.information(None, 'Connected',
                                    "Successfully connected, you may now close connection dialog", QMessageBox.Ok)

            self.conn_ui.connectionProgress.setMaximum(100)
            self.conn_ui.connectionProgress.setValue(100)
            self.conn_ui.connectionProgress.setFormat("Connected")
            self.conn_ui.connectButton.setDisabled(True)
            self.main_ui.sendButton.setDisabled(False)
            self.main_ui.connectionButton.setText("Disconnect")
            self.main_ui.connectionButton.clicked.connect(self.disconnect)
            self.main_ui.roomsButton.show()

            self.listening_thread = Thread(target=self.listen)
            self.listening_thread.start()

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
        self.socket.send(bytes("\\quit", "utf8"))
        if self.listening_thread.isAlive():
            self.listening_thread.join(1)
        self.socket.shutdown(2)
        self.socket.close()
        QMessageBox.information(None, 'Disconnected',
                                "Disconnected successfully", QMessageBox.Ok)
        self.main_ui.connectionButton.setText("Connection")
        self.main_ui.sendButton.setDisabled(True)
        self.main_ui.connectionButton.clicked.disconnect(self.disconnect)
        self.conn_ui.connectionProgress.setMaximum(0)
        self.conn_ui.connectionProgress.setValue(-1)
        self.conn_ui.connectionProgress.hide()
        self.conn_ui.connectButton.setDisabled(False)
        self.main_ui.roomsButton.hide()

    def listen(self):
        """Listens for server messages"""
        proceed = True
        while proceed:
            try:
                message = self.socket.recv(self.buffer_size).decode("utf8")
                proceed = self.treat_message(message)
            except OSError:  # Client has left
                break

    def send(self, message):
        self.socket.send(bytes(message, "utf8"))

    def send_action(self):
        message = self.main_ui.read_message_box()
        self.send(message)
        self.main_ui.clear_message_box()

    def create_room(self):
        room = self.rooms_ui.roomNameEdit.text()
        self.socket.send(bytes("\\create{%s}" % room, "utf8"))
        self.get_rooms()

    def create_user(self):
        nick = self.rooms_ui.displayNameEdit.text()
        self.socket.send(bytes("\\insert{%s}" % nick, "utf8"))
        self.rooms_ui.displayNameEdit.setDisabled(True)
        self.rooms_ui.saveButton.setDisabled(True)
        self.get_rooms()

    def get_rooms(self):
        self.socket.send(bytes("\\rooms", "utf8"))

    def get_users(self, item):
        room = item.text()
        self.socket.send(bytes("\\online{%s}" % room, "utf8"))

    def join_room(self):
        item = self.rooms_ui.roomsList.currentItem()
        if item is not None:
            self.socket.send(bytes("\\join{%s}" % item.text(), "utf8"))
            self.rooms_ui.leaveButton.setDisabled(False)
            self.rooms_ui.joinButton.setDisabled(True)
        else:
            QMessageBox.warning(None, "Joining a room", "You must select a room", QMessageBox.Ok)

    def leave_room(self):
        self.socket.send(bytes("\\leave", "utf8"))
        self.rooms_ui.leaveButton.setDisabled(True)
        self.rooms_ui.joinButton.setDisabled(False)

    def treat_message(self, message):
        answer = True
        match = self.answers_regexp.match(message)
        if match:
            command, answer = match.groups()
            if command == "insert":
                if answer == "not_valid_nickname":
                    QMessageBox.critical(None, "Login",
                                         "Nickname not valid", QMessageBox.Ok)
            elif command == "quit":
                if answer == "success":
                    answer = False

            elif command == "rooms":
                if answer != "":
                    print(answer)
                    self.rooms_ui.clear_rooms()
                    for room in answer.split("|"):
                        self.rooms_ui.add_room(room)
                else:
                    self.rooms_ui.clear_rooms()

            elif command == "online":
                if answer == "no_room":
                    QMessageBox.critical(None, "Online",
                                         "You must specify a room", QMessageBox.Ok)
                else:
                    if answer != "":
                        print(answer)
                        self.rooms_ui.clear_users()
                        for user in answer.split("|"):
                            self.rooms_ui.add_user(user)
                    else:
                        self.rooms_ui.clear_users()

            elif command == "server":
                if answer == "no_room":
                    QMessageBox.critical(None, "Sending",
                                         "You must join a room first", QMessageBox.Ok)
            elif command == "join":
                if answer == "failure":
                    QMessageBox.critical(None, "Joining room",
                                         "Room does not exists", QMessageBox.Ok)
            elif command == "leave":
                if answer == "no_room":
                    QMessageBox.critical(None, "Leaving room",
                                         "You are not in a room", QMessageBox.Ok)
            elif command == "create":
                if answer == "success":
                    QMessageBox.information(None, "Creating room",
                                            "Room successfully created", QMessageBox.Ok)
                elif answer == "failure":
                    QMessageBox.critical(None, "Creating room",
                                         "Room already exists", QMessageBox.Ok)
        else:
            self.main_ui.write_message(message)
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