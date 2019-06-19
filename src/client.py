# Project imports
# Python built-in for sockets programming
import sys
from socket import *

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QDialog

from src.client_ui import ClientWindow, Ui_MainWindow
from src.connect_ui import Ui_connectionDialog
from src.rooms_ui import Ui_roomsDialog


class Client:
    """Handles the communication with the server application"""

    buffer_size = 1024

    def __init__(self, ui_obj, host, port, is_tcp):
        """Initializes the client side application with a given host and port"""
        # Socket properties
        self.conn_host = host
        self.conn_port = port
        self.conn_address = (self.conn_host, self.conn_port)
        self.socket = socket(AF_INET, SOCK_STREAM if is_tcp else SOCK_DGRAM)

        # UI object
        self.ui_obj = ui_obj

    def connect(self):
        self.socket.connect(self.conn_address)

    def disconnect(self):
        self.socket.shutdown(2)
        self.socket.close()

    def receive(self):
        while True:
            try:
                message = self.socket.recv(self.buffer_size).decode("utf8")
            except OSError:  # Client has left
                break

    def send(self, message):
        self.socket.send(bytes(message, "utf8"))

    def send_action(self):
        message = self.ui_obj.read_message_box()
        self.send(message)

    def treat_message(self, message):
        print()


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

    # Application initial configuration
    main_ui.connectionButton.clicked.connect(conn_dialog.show)
    main_ui.roomsButton.clicked.connect(rooms_dialog.show)

    # Application initial size
    main_window.resize(1024, 768)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())