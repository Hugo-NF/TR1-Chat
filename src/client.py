# Project imports
# Python built-in for sockets programming
import sys
from socket import *

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

    conn_ui.connectButton.clicked.connect(conn_ui.start_animation)
    main_ui.actionAbout_Qt.triggered.connect(app.aboutQt)

    # Application initial size
    main_window.resize(1024, 768)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())